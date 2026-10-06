"""
DRF 统一响应构建与视图基类。

所有业务视图统一继承 ``StandardAPIView``(禁止直接继承 ``APIView``),
以获得统一响应格式、分页能力与便捷方法。

统一响应格式::

    {
        "code": <HTTP 状态码>,
        "message": "<提示信息>",
        "data": <业务数据>,
        "requestId": "<本次请求唯一 ID>"
    }

其中 ``requestId`` 由 ``RequestLogMiddleware`` 在请求入口写入线程本地存储,
此处构建响应时自动读取注入,实现前后端日志链路关联,无需各视图手动传递。
"""

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from Backend.utils.drf.pagination import StandardPageNumberPagination
from Backend.utils.log.request_id import get_request_id

# ═══════════════════════════════════════════════════════════════════════════════
# 统一响应构建工具
# ═══════════════════════════════════════════════════════════════════════════════


def _build_payload(code, message, data):
    """构建统一响应体字典,自动注入当前请求的 requestId。"""
    return {
        "code": code,
        "message": message,
        "data": {} if data is None else data,
        "requestId": get_request_id(),
    }


def success_response(data=None, message="success", status_code=200):
    """构建统一成功响应。

    Parameters
    ----------
    data : dict | list | None
        业务数据,为 None 时填充空字典 ``{}``
    message : str
        提示信息,默认 ``"success"``
    status_code : int
        HTTP 状态码,默认 ``200``

    Returns
    -------
    Response
        ``{"code", "message", "data", "requestId"}`` 格式响应
    """
    return Response(_build_payload(status_code, message, data), status=status_code)


def error_response(message, status_code=400, data=None):
    """构建统一错误响应。

    Parameters
    ----------
    message : str
        错误提示信息,必传
    status_code : int
        HTTP 状态码,默认 ``400``
    data : dict | None
        附加错误详情,为 None 时填充空字典 ``{}``

    Returns
    -------
    Response
        ``{"code", "message", "data", "requestId"}`` 格式响应
    """
    return Response(_build_payload(status_code, message, data), status=status_code)


# ═══════════════════════════════════════════════════════════════════════════════
# 可复用序列化器校验工具
# ═══════════════════════════════════════════════════════════════════════════════


def make_fk_validator(queryset, label, *, allow_null=False):
    """生成 FK 存在性校验方法,可直接赋值为 Serializer 的 ``validate_<field>``。"""

    def validator(self, value):
        if allow_null and value is None:
            return value
        if not queryset.filter(id=value).exists():
            raise serializers.ValidationError(f"{label}不存在")
        return value

    return validator


# ═══════════════════════════════════════════════════════════════════════════════
# 统一视图基类
# ═══════════════════════════════════════════════════════════════════════════════


class StandardAPIView(APIView):
    """项目统一视图基类,为所有接口提供标准化响应与分页能力。

    便捷方法:
    - ``self.success()``：构建统一成功响应
    - ``self.error()``：构建统一错误响应
    - ``self.paginate()``：对查询集执行分页并序列化
    - ``self.get_object_or_error()``：按主键取对象,不存在返回 404 错误响应
    - ``self.update_instance()``：将校验数据批量赋值到模型实例(部分更新)

    业务视图应通过这些便捷方法返回统一结构,避免各接口自行拼接响应体。
    """

    pagination_class = StandardPageNumberPagination

    def success(self, data=None, message="success", status_code=200):
        """返回统一成功响应。"""
        return success_response(data=data, message=message, status_code=status_code)

    def error(self, message, status_code=400, data=None):
        """返回统一错误响应。"""
        return error_response(message=message, status_code=status_code, data=data)

    def get_object_or_error(self, model_or_qs, pk, label="资源"):
        """按主键查找记录,不存在时返回 ``(None, 404 错误响应)``。

        Returns
        -------
        tuple[Model | None, Response | None]
            ``(实例, None)`` 表示找到;``(None, error_response)`` 表示未找到。

        调用方应先判断第二个返回值;不为 ``None`` 时直接返回该错误响应。
        """
        qs = model_or_qs.objects if hasattr(model_or_qs, "objects") else model_or_qs
        obj = qs.filter(id=pk).first()
        if obj is None:
            return None, self.error(f"{label}不存在", status_code=404)
        return obj, None

    def paginate(self, request, queryset, serializer_class, context=None):
        """对查询集执行统一分页并序列化。

        Returns
        -------
        Response
            统一格式响应,data 结构为 ``{"count", "page", "page_size", "results"}``
        """
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = serializer_class(page, many=True, context=context or {"request": request})
        return self.success(paginator.get_paginated_data(serializer.data))

    @staticmethod
    def update_instance(instance, validated_data, fields):
        """将序列化器校验后的数据批量赋值到模型实例(仅赋值出现的字段)。

        **不自动调用 save()**,调用方在赋值后自行保存,
        以便保存前做额外处理(如密码哈希)。
        """
        for field in fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
