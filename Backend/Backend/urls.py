"""
Backend 项目根路由。

挂载:
- ``admin/``：Django Admin 后台(SimpleUI 美化)
- ``auth/``：账户认证接口(登录/注册/当前用户/登出/刷新)
- ``swagger/`` / ``redoc/``：接口文档

前端经 Vite 代理(``/api`` → 后端,rewrite 去掉 ``/api``),
故前端 ``/api/auth/login/`` 实际命中后端 ``/auth/login/``。
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Backend API",
        default_version="v1",
        description="项目接口文档",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("Account.urls")),
    path("swagger.<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
