"""
JWT 令牌服务。

本项目采用纯 JWT 双令牌方案:

- ``access_token``：短效令牌,用于接口鉴权
- ``refresh_token``：长效令牌,用于续签新的 access_token
- 服务端唯一状态保存在 ``User.token_version``,递增后该用户历史令牌全部失效

令牌载荷(payload)字段:
    access:  token_type / user_id / username / role / token_version / exp / iat / jti
    refresh: token_type / user_id / token_version / exp / iat / jti

依赖 settings 配置项(见 settings/base.py 的 JWT 段):
- ``JWT_SECRET_KEY``：签名密钥(默认回退到 SECRET_KEY)
- ``JWT_ALGORITHM``：签名算法,默认 HS256
- ``JWT_ACCESS_TOKEN_TTL_MINUTES``：access 有效期(分钟),默认 30
- ``JWT_REFRESH_TOKEN_TTL_DAYS``：refresh 有效期(天),默认 7
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# JWT 的 exp/iat 使用 UTC 绝对时间点
UTC = timezone(timedelta(0))


def _secret_key():
    """JWT 签名密钥,未单独配置时回退到 Django SECRET_KEY。"""
    return getattr(settings, "JWT_SECRET_KEY", None) or settings.SECRET_KEY


def _algorithm():
    return getattr(settings, "JWT_ALGORITHM", "HS256")


def _access_ttl_minutes():
    return getattr(settings, "JWT_ACCESS_TOKEN_TTL_MINUTES", 30)


def _refresh_ttl_days():
    return getattr(settings, "JWT_REFRESH_TOKEN_TTL_DAYS", 7)


class TokenService:
    """负责 access / refresh 令牌的签发、解析、轮换与失效。"""

    access_required_claims = ["token_type", "user_id", "token_version", "exp", "iat"]
    refresh_required_claims = access_required_claims

    # ── 过期时间计算 ──

    @classmethod
    def _access_expire_at(cls):
        return datetime.now(UTC) + timedelta(minutes=_access_ttl_minutes())

    @classmethod
    def _refresh_expire_at(cls):
        return datetime.now(UTC) + timedelta(days=_refresh_ttl_days())

    @classmethod
    def _expires_in(cls):
        """access token 过期秒数,随令牌一并返回给前端。"""
        return int(_access_ttl_minutes() * 60)

    # ── 编解码 ──

    @classmethod
    def _encode(cls, payload):
        return jwt.encode(payload, _secret_key(), algorithm=_algorithm())

    @classmethod
    def _build_payload(cls, user, token_type):
        """构建统一 JWT 载荷。"""
        now = datetime.now(UTC)
        expire_at = cls._access_expire_at() if token_type == "access" else cls._refresh_expire_at()
        payload = {
            "token_type": token_type,
            "user_id": user.id,
            "token_version": user.token_version,
            "exp": expire_at,
            "iat": now,
            "jti": uuid4().hex,
        }
        # access 令牌额外携带展示/鉴权所需的轻量信息
        if token_type == "access":
            payload["username"] = user.username
            payload["role"] = user.role
        return payload

    @classmethod
    def _decode(cls, token, required_claims, token_type, *, include_user=False):
        """解码 JWT,并校验类型、用户状态与 token_version。

        Raises
        ------
        jwt.InvalidTokenError
            类型不符、用户不存在/停用、token_version 不匹配时抛出。
            (``jwt.ExpiredSignatureError`` 是其子类,由调用方区分处理)
        """
        payload = jwt.decode(
            token,
            _secret_key(),
            algorithms=[_algorithm()],
            options={"require": required_claims},
        )
        if payload.get("token_type") != token_type:
            raise jwt.InvalidTokenError(f"invalid {token_type} token type")

        user = User.objects.filter(id=payload.get("user_id")).first()
        if user is None:
            raise jwt.InvalidTokenError("user not found")
        if getattr(user, "status", "active") != "active" or not user.is_active:
            raise jwt.InvalidTokenError("user disabled")
        if user.token_version != payload.get("token_version"):
            raise jwt.InvalidTokenError("token version mismatch")

        if include_user:
            return payload, user
        return payload

    # ── 对外签发 ──

    @classmethod
    def build_access_token(cls, user):
        """签发 access token。"""
        return cls._encode(cls._build_payload(user, "access"))

    @classmethod
    def build_refresh_token(cls, user):
        """签发 refresh token。"""
        return cls._encode(cls._build_payload(user, "refresh"))

    @classmethod
    def issue_token_pair(cls, user):
        """签发 access + refresh 令牌对。

        Returns
        -------
        dict
            ``{"access_token", "refresh_token", "expires_in"}``
        """
        return {
            "access_token": cls.build_access_token(user),
            "refresh_token": cls.build_refresh_token(user),
            "expires_in": cls._expires_in(),
        }

    # ── 对外解析 ──

    @classmethod
    def parse_access_token(cls, token):
        """解析 access token,返回 payload。"""
        return cls._decode(token, cls.access_required_claims, "access")

    @classmethod
    def parse_access_token_with_user(cls, token):
        """解析 access token,返回 ``(payload, user)``。"""
        return cls._decode(token, cls.access_required_claims, "access", include_user=True)

    @classmethod
    def parse_refresh_token(cls, token):
        """解析 refresh token,返回 payload。"""
        return cls._decode(token, cls.refresh_required_claims, "refresh")

    # ── 轮换与失效 ──

    @classmethod
    def rotate_refresh_token(cls, raw_refresh_token):
        """用 refresh token 续签新的 access token。

        Returns
        -------
        dict | None
            成功返回 ``{"access_token", "expires_in"}``;
            refresh 无效/过期/已撤销时返回 None。
        """
        try:
            payload, user = cls._decode(
                raw_refresh_token, cls.refresh_required_claims, "refresh", include_user=True
            )
        except jwt.InvalidTokenError:
            return None
        return {
            "access_token": cls.build_access_token(user),
            "expires_in": cls._expires_in(),
        }

    @classmethod
    def revoke_user_tokens(cls, user):
        """递增用户 token_version,使其历史 access/refresh 令牌全部失效。

        用于登出、改密、强制下线。直接传入已认证的 user 对象即可。
        """
        user.bump_token_version()
        return True
