"""
自定义 Bearer Token 认证后端。

实现项目的 PyJWT Bearer 认证,替代 DRF 默认的 Session / Token 认证。

认证流程:
1. 从请求头 ``Authorization: Bearer <token>`` 提取 token
2. 通过 ``TokenService.parse_access_token_with_user()`` 解码并校验
   签名、过期时间、用户状态与 token_version
3. 返回 ``(user, payload)`` 元组,DRF 自动注入到 ``request.user`` / ``request.auth``

约定:
- Bearer 关键字严格大小写匹配(RFC 7235)
- 请求头无 Authorization 时返回 None(跳过本认证,交由权限类决定是否拒绝)
- token 过期、无效、用户停用时抛出 AuthenticationFailed(返回 401)

启用方式:
    settings 中配置
    ``REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] =
      ["Backend.utils.auth.authentication.BearerTokenAuthentication"]``
"""

import jwt
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from Backend.utils.auth.token_service import TokenService


class BearerTokenAuthentication(authentication.BaseAuthentication):
    """校验 access token,并还原当前登录用户。

    DRF 认证后端约定:
    - 返回 ``(user, auth)`` 元组表示认证成功
    - 返回 ``None`` 表示跳过该认证后端(不拦截)
    - 抛出 ``AuthenticationFailed`` 表示认证失败(返回 401)
    """

    keyword = "Bearer"

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).decode("utf-8")
        if not header:
            return None
        parts = header.split(" ")
        if len(parts) != 2 or parts[0] != self.keyword:
            raise AuthenticationFailed("Authorization 头格式错误")

        token = parts[1]
        try:
            payload, user = TokenService.parse_access_token_with_user(token)
        except jwt.ExpiredSignatureError as exc:
            raise AuthenticationFailed("access_token 已过期") from exc
        except jwt.InvalidTokenError as exc:
            raise AuthenticationFailed("access_token 无效") from exc

        return user, payload

    def authenticate_header(self, request):
        """返回 WWW-Authenticate 头,使未认证响应为 401 而非 403。"""
        return self.keyword
