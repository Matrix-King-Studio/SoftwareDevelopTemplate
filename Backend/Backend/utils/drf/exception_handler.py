"""
自定义 DRF 全局异常处理器。

职责:
- 拦截所有 DRF 已处理和未处理的异常
- 统一转换为 ``{"code", "message", "data": {}, "requestId"}`` 格式
- 修正认证失败的 403→401 状态码
- 捕获数据库异常并返回 507
- 捕获 Redis 缓存异常并返回 507
- 兜底未知异常返回 500

启用方式:
    settings 中配置
    ``REST_FRAMEWORK["EXCEPTION_HANDLER"] = "Backend.utils.drf.exception_handler.custom_exception_handler"``

说明:
    所有响应体的 ``requestId`` 字段从线程本地存储读取(由 RequestLogMiddleware 写入),
    保证错误响应同样携带 requestId,便于前后端日志关联排查。
"""

import logging

from django.db import DatabaseError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from Backend.utils.log.request_id import get_request_id

logger = logging.getLogger("django")

# redis 为可选依赖:未安装时不影响异常处理主流程
try:
    from redis.exceptions import RedisError
except ImportError:  # pragma: no cover - redis 未安装时的降级
    RedisError = None


def _make_response(code, message):
    """构建统一格式错误响应,自动注入 requestId。"""
    return Response(
        {"code": code, "message": message, "data": {}, "requestId": get_request_id()},
        status=code,
    )


def _describe_context(context):
    """从 DRF 异常上下文中提取请求摘要,用于错误日志排查。

    Parameters
    ----------
    context : dict
        DRF 异常上下文,含 ``request`` / ``view`` 等。

    Returns
    -------
    str
        形如 ``POST /auth/login/ view=LoginView`` 的摘要;
        requestId 由 logging 过滤器自动注入,无需在此拼接。
    """
    request = context.get("request")
    view = context.get("view")
    method = getattr(request, "method", "-")
    path = getattr(request, "path", "-")
    view_name = type(view).__name__ if view is not None else "-"
    return f"{method} {path} view={view_name}"


# ── DRF 错误详情提取(dict / list / str 三种结构) ──


def _extract_from_dict(detail):
    """从字典结构的 DRF 错误详情中提取可读消息。

    例如 ``{"username": ["该字段是必填项。"], "non_field_errors": ["密码错误"]}``
    """
    messages = []
    for key, value in detail.items():
        inner = _extract_error_messages(value)
        # non_field_errors 不带字段前缀
        messages.append(inner if key == "non_field_errors" else f"{key}: {inner}")
    return "; ".join(filter(None, messages))


def _extract_from_list(detail):
    """从列表结构的 DRF 错误详情中提取消息。"""
    return "; ".join(str(item) for item in detail)


def _extract_error_messages(detail):
    """递归提取 DRF 错误详情为可读字符串(处理 dict / list / str 三种结构)。"""
    if isinstance(detail, dict):
        return _extract_from_dict(detail)
    if isinstance(detail, list):
        return _extract_from_list(detail)
    return str(detail)


def _wrap_response_data(raw):
    """将 DRF 默认错误响应体转换为统一 message 字符串。"""
    if isinstance(raw, dict) and "detail" in raw:
        return str(raw["detail"])
    if isinstance(raw, dict):
        return _extract_error_messages(raw)
    if isinstance(raw, list):
        return "; ".join(str(item) for item in raw)
    return str(raw)


def custom_exception_handler(exc, context):
    """自定义全局异常处理器,保证所有响应为统一格式。

    处理顺序:
    1. 委托 DRF 默认处理器处理已知异常
    2. 捕获 DRF 不处理的数据库异常 → 507
    3. 捕获 DRF 不处理的 Redis 缓存异常 → 507
    4. 包装 DRF 已处理的响应为统一格式(并修正 403→401)
    5. 兜底未处理异常 → 500
    """
    # ── 步骤 1:委托 DRF 默认处理器 ──
    response = drf_exception_handler(exc, context)
    where = _describe_context(context)

    # ── 步骤 2:数据库异常 ──
    if response is None and isinstance(exc, DatabaseError):
        logger.error("DatabaseError | %s | %s: %s", where, type(exc).__name__, exc, exc_info=True)
        return _make_response(status.HTTP_507_INSUFFICIENT_STORAGE, "数据库错误")

    # ── 步骤 3:Redis 缓存异常 ──
    if response is None and RedisError is not None and isinstance(exc, RedisError):
        logger.error("RedisError | %s | %s: %s", where, type(exc).__name__, exc, exc_info=True)
        return _make_response(status.HTTP_507_INSUFFICIENT_STORAGE, "缓存服务异常")

    # ── 步骤 4:包装 DRF 已处理的响应 ──
    if response is not None:
        # 403→401 修正:仅针对认证失败,不影响真正的权限拒绝
        if response.status_code == status.HTTP_403_FORBIDDEN and isinstance(
            exc, AuthenticationFailed | NotAuthenticated
        ):
            response.status_code = status.HTTP_401_UNAUTHORIZED

        raw = response.data
        # 已是统一格式则只补 requestId 后返回,避免重复包装
        if isinstance(raw, dict) and "code" in raw and "message" in raw:
            raw.setdefault("requestId", get_request_id())
            return response

        response.data = {
            "code": response.status_code,
            "message": _wrap_response_data(raw),
            "data": {},
            "requestId": get_request_id(),
        }
        return response

    # ── 步骤 5:兜底未处理异常 ──
    logger.error("Unhandled exception | %s | %s: %s", where, type(exc).__name__, exc, exc_info=True)
    return _make_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "服务器内部错误")
