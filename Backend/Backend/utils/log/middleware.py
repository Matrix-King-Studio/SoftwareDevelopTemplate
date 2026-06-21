"""
请求日志中间件。

``RequestLogMiddleware`` 职责:
1. 在请求入口生成/复用 requestId(优先复用前端注入的 ``X-Trace-Id``)
   并写入线程本地存储,供统一响应构建与异常处理读取
2. 将 requestId 写入响应头 ``X-Request-Id``,贯通前后端日志链路
3. 记录每个请求的方法、路径、状态码、耗时、用户标识
4. 错误请求(4xx/5xx)自动附带客户端 IP、Query 参数、脱敏后的请求体摘要
5. 请求结束后清理线程本地的 requestId,避免线程复用串号

放置位置:应在 ``AuthenticationMiddleware`` 之后,以便获取 request.user。
"""

import json
import logging
import time

from django.conf import settings

from Backend.utils.log.request_id import (
    clear_request_id,
    generate_request_id,
    set_request_id,
)

request_logger = logging.getLogger("request")

SKIP_LOG_PREFIXES = ("/static/", "/media/")
MAX_BODY_LENGTH = 512

# 请求体脱敏字段
_SENSITIVE_FIELDS = frozenset(
    {
        "password",
        "password1",
        "password2",
        "old_password",
        "new_password",
        "confirm_password",
        "token",
        "access_token",
        "refresh_token",
    }
)


def _get_client_ip(request):
    """提取客户端真实 IP,优先 X-Forwarded-For(反向代理场景)。"""
    meta = getattr(request, "META", {})
    forwarded = meta.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return meta.get("REMOTE_ADDR")


def _sanitize(data):
    """递归脱敏请求体中的敏感字段(返回新对象,不改原数据)。"""
    if isinstance(data, dict):
        return {k: "***" if k in _SENSITIVE_FIELDS else _sanitize(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_sanitize(item) for item in data]
    return data


class RequestLogMiddleware:
    """记录请求摘要,并管理 requestId 的生成、注入与清理。"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._should_skip(request.path):
            return self.get_response(request)

        # ── 生成/复用 requestId 并写入线程本地 ──
        request_id = request.META.get("HTTP_X_TRACE_ID") or generate_request_id()
        set_request_id(request_id)

        start = time.monotonic()
        try:
            response = self.get_response(request)
            duration_ms = (time.monotonic() - start) * 1000
            # 回写响应头,贯通前后端链路
            response["X-Request-Id"] = request_id
            self._log_request(request, response, duration_ms)
            return response
        finally:
            # 必须清理,避免同线程下次请求串号
            clear_request_id()

    def process_exception(self, request, exception):
        """补充未被 DRF 处理的异常上下文,不拦截异常。"""
        if self._should_skip(request.path):
            return None
        request_logger.error(
            "未处理异常 | %s %s | user=%s | ip=%s | %s: %s\n%s",
            request.method,
            request.path,
            self._get_user_id(request),
            _get_client_ip(request),
            type(exception).__name__,
            exception,
            self._build_context(request),
            exc_info=True,
        )
        return None

    def _log_request(self, request, response, duration_ms):
        """按状态码选择日志级别输出请求摘要。

        requestId 由 logging 的 RequestIDFilter 自动注入到每条日志,
        此处无需手动拼接,故格式串不含 rid 字段。
        """
        status_code = response.status_code
        user_id = self._get_user_id(request)
        base_msg = "%s %s %d %.0fms user=%s"
        base_args = (request.method, request.path, status_code, duration_ms, user_id)

        if status_code >= 500:
            request_logger.error(
                base_msg + " ip=%s\n%s",
                *base_args,
                _get_client_ip(request),
                self._build_context(request),
            )
        elif status_code >= 400:
            request_logger.warning(
                base_msg + " ip=%s\n%s",
                *base_args,
                _get_client_ip(request),
                self._build_context(request),
            )
        elif duration_ms >= getattr(settings, "REQUEST_LOG_SUCCESS_MIN_DURATION_MS", 0):
            request_logger.info(base_msg, *base_args)

    @staticmethod
    def _build_context(request):
        """构建错误请求的详细上下文(Query 参数 + 脱敏请求体摘要)。"""
        parts = []
        query = request.GET.dict()
        if query:
            parts.append(f"  Query: {query}")
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                raw = request.data if hasattr(request, "data") else {}
                body = _sanitize(raw if isinstance(raw, dict | list) else json.loads(raw))
                body_str = str(body)
                if len(body_str) > MAX_BODY_LENGTH:
                    body_str = body_str[:MAX_BODY_LENGTH] + "...(truncated)"
                parts.append(f"  Body: {body_str}")
            except Exception:  # noqa: BLE001
                parts.append("  Body: <unreadable>")
        return "\n".join(parts) if parts else "  (no extra context)"

    @staticmethod
    def _should_skip(path):
        return path.startswith(SKIP_LOG_PREFIXES)

    @staticmethod
    def _get_user_id(request):
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            return user.pk
        return "anonymous"
