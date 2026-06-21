"""
账户应用路由。

路径与前端 ``Frontend/src/api/modules/account.ts`` 对齐。
本应用在根 urls.py 中以 ``auth/`` 前缀挂载,故前端经 Vite 代理
(``/api`` → 后端,且 rewrite 去掉 ``/api``)后,实际命中:

    /api/auth/login/         → /auth/login/
    /api/auth/registration/  → /auth/registration/
    /api/auth/user/          → /auth/user/
    /api/auth/logout/        → /auth/logout/
    /api/auth/token/refresh/ → /auth/token/refresh/
"""

from django.urls import path

from Account.views import (
    CurrentUserView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    RegisterView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("registration/", RegisterView.as_view(), name="auth-registration"),
    path("user/", CurrentUserView.as_view(), name="auth-current-user"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("token/refresh/", RefreshTokenView.as_view(), name="auth-token-refresh"),
]
