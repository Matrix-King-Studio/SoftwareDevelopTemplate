"""
请求 ID(requestId)管理。

基于线程本地存储(thread-local)在"单次请求"范围内保存 request_id,
使得不持有 request 对象的代码(如统一响应构建函数 success_response、
全局异常处理器)也能取到当前请求的 requestId 并注入响应体。

写入时机:
    由 ``RequestLogMiddleware`` 在请求进入时设置(优先复用前端注入的
    ``X-Trace-Id``,缺失时生成新的 uuid),请求结束时清理。

读取时机:
    ``success_response`` / ``error_response`` / ``custom_exception_handler``
    在构建响应体时读取,写入到响应的 ``requestId`` 字段。

注意:
    线程本地变量在同一线程的请求间必须显式清理,否则可能串号。
    中间件已在 finally 中调用 ``clear_request_id()`` 保证清理。
"""

import logging
import threading
from uuid import uuid4

_local = threading.local()


def set_request_id(request_id: str) -> None:
    """写入当前线程的 request_id。"""
    _local.request_id = request_id


def get_request_id(default: str = "") -> str:
    """读取当前线程的 request_id,未设置时返回 default。"""
    return getattr(_local, "request_id", default)


def clear_request_id() -> None:
    """清理当前线程的 request_id,避免线程复用时串号。"""
    if hasattr(_local, "request_id"):
        del _local.request_id


def generate_request_id() -> str:
    """生成一个新的 request_id(无连字符的 uuid4 十六进制串)。"""
    return uuid4().hex


class RequestIDFilter(logging.Filter):
    """日志过滤器:为每条日志记录自动注入 ``request_id`` 字段。

    挂载到 LOGGING 的 handler/formatter 后,所有在请求线程内产生的日志
    (请求日志、全局异常日志、业务代码的 logger 调用)都会带上当前请求的
    requestId,与响应体的 ``requestId`` / 响应头 ``X-Request-Id`` 完全一致,
    从而实现"一个 requestId 串起前端响应 → 后端请求日志 → 错误堆栈"的排查链路。

    不在请求上下文中的日志(如启动日志、定时任务)``request_id`` 为 ``"-"``。
    """

    def filter(self, record):
        record.request_id = get_request_id(default="-")
        return True
