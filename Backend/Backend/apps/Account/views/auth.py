"""
账户认证接口。

提供注册、登录、获取当前用户、登出、刷新令牌五个接口,
全部继承 ``StandardAPIView``,响应统一为 ``{code, message, data, requestId}``。

认证方案:纯 JWT(access + refresh),见 Backend/utils/auth/token_service.py。
接口路径在 Account/urls.py 中映射,与前端 src/api/modules/account.ts 对齐。
"""

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from Account.serializers import (
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
    UserInfoSerializer,
)
from Backend.utils.auth.token_service import TokenService
from Backend.utils.drf.api import StandardAPIView

User = get_user_model()


def _login_payload(user):
    """构建登录/注册成功的统一返回数据:令牌对 + 用户信息。

    结构对应前端 ``AuthTokens``:``{access_token, refresh_token, expires_in, user}``。
    """
    tokens = TokenService.issue_token_pair(user)
    tokens["user"] = UserInfoSerializer(user).data
    return tokens


class RegisterView(StandardAPIView):
    """
    用户注册。

    URL: POST /auth/registration/
    认证: 无需认证(公开接口)

    请求参数(Body):
        - username (str, 必传): 用户名,唯一
        - email (str, 可选): 邮箱
        - password1 (str, 必传): 密码,至少 6 位
        - password2 (str, 必传): 确认密码,需与 password1 一致

    返回:
        成功(200): data 包含 access_token / refresh_token / expires_in / user
        失败(400): 用户名已存在、两次密码不一致等
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return self.success(_login_payload(user), message="注册成功")


class LoginView(StandardAPIView):
    """
    用户登录(用户名 + 密码)。

    URL: POST /auth/login/
    认证: 无需认证(公开接口)
    限流: login 作用域(默认 10/min)

    请求参数(Body):
        - username (str, 必传): 用户名
        - password (str, 必传): 密码

    返回:
        成功(200): data 包含 access_token / refresh_token / expires_in / user
        失败(400): 用户名或密码错误
        失败(403): 账号已停用
    """

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return self.error("用户名或密码错误")
        if user.status != "active" or not user.is_active:
            return self.error("账号已停用", status_code=403)

        return self.success(_login_payload(user), message="登录成功")


class CurrentUserView(StandardAPIView):
    """
    获取当前登录用户信息。

    URL: GET /auth/user/
    认证: 需要 access token

    返回:
        成功(200): data 为当前用户信息(UserInfo)
        失败(401): 未登录或 token 无效/过期
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.success(UserInfoSerializer(request.user).data, message="查询成功")


class LogoutView(StandardAPIView):
    """
    退出登录。

    URL: POST /auth/logout/
    认证: 需要 access token

    通过递增当前用户的 token_version,使其历史 access/refresh token 全部失效。
    前端无需在 body 中携带 refresh_token,直接用当前 access token 识别用户。

    返回:
        成功(200): message="退出成功"
        失败(401): 未登录或 token 无效/过期
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        TokenService.revoke_user_tokens(request.user)
        return self.success(message="退出成功")


class RefreshTokenView(StandardAPIView):
    """
    使用 refresh token 续签 access token。

    URL: POST /auth/token/refresh/
    认证: 无需 access token,使用 refresh token

    请求参数(Body):
        - refresh_token (str, 必传): 登录时返回的 refresh token

    返回:
        成功(200): data 包含新的 access_token 及 expires_in
        失败(401): refresh_token 无效、已过期或已撤销
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = TokenService.rotate_refresh_token(serializer.validated_data["refresh_token"])
        if payload is None:
            return self.error("refresh_token 无效、已过期或已撤销", status_code=401)
        return self.success(payload, message="刷新成功")
