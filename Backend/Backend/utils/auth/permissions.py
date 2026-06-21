"""
通用权限类。

本模板提供两类常用权限:

1. ``IsActiveUser``：要求已认证且账号状态为启用(active)
2. ``IsAdminRole``：要求已认证且角色为管理员(role=admin)

视图通过 ``permission_classes`` 引用即可,例如::

    class MyView(StandardAPIView):
        permission_classes = [IsActiveUser]

DRF 自带的 ``IsAuthenticated`` / ``AllowAny`` 可按需直接使用。
企业项目如需更细粒度的"角色→模块"映射权限,可在此文件按需扩展。
"""

from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    """要求已认证,且账号状态为 active。

    认证后端已拦截停用账号,此权限作为视图层的二次保险,
    同时让"未登录"返回 401、"已登录但被停用"返回 403,语义清晰。
    """

    message = "账号未登录或已停用"

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "status", "active") == "active"


class IsAdminRole(BasePermission):
    """要求已认证且角色为管理员(role=admin)。"""

    message = "需要管理员权限"

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "role", None) == "admin"
