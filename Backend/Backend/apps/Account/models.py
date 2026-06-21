"""
账户模型。

本模板采用自定义 ``User`` 模型(继承 Django ``AbstractUser``),
在 Django 自带的 username / email / password / 权限体系之上,
扩展企业项目常用的三个字段:

- ``role``：业务角色,用于接口级角色权限控制(见 utils/auth/permissions.py)
- ``status``：账号启用状态,停用后即使 token 未过期也无法通过鉴权
- ``token_version``：令牌版本号,递增即可使该用户历史签发的所有
  access / refresh token 全部失效(用于"登出""改密""强制下线")

为什么继承 AbstractUser:
    模板的登录/注册走 username + password,且需要 Django Admin、SimpleUI,
    AbstractUser 与这些设施天然兼容,改动最小。settings 中通过
    ``AUTH_USER_MODEL = "Account.User"`` 指定本模型为项目用户模型。

注意:
    必须在项目"首次 migrate 之前"就指定 AUTH_USER_MODEL,
    本模板正是零迁移状态下落地,故安全。后续若要改动 User 字段,
    按常规 makemigrations / migrate 流程即可。
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """平台用户。

    继承 AbstractUser 已自带的字段:
        username / first_name / last_name / email / password /
        is_staff / is_active / is_superuser / last_login / date_joined / groups / user_permissions

    本模型新增的业务字段见下方。
    """

    ROLE_CHOICES = [
        ("user", "普通用户"),
        ("admin", "管理员"),
    ]

    STATUS_CHOICES = [
        ("active", "启用"),
        ("disabled", "停用"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user",
        verbose_name="角色",
        help_text="user=普通用户,admin=管理员;用于接口级角色权限控制",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="账号状态",
        help_text="active=启用,disabled=停用;停用后即使 token 未过期也无法通过鉴权",
    )
    token_version = models.IntegerField(
        default=0,
        verbose_name="Token 版本号",
        help_text="递增后可使该用户历史 access/refresh token 全部失效(登出/改密/强制下线)",
    )
    avatar = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="头像",
        help_text="头像图片相对路径或 URL",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "t_user"
        verbose_name = "平台用户"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["role"], name="idx_user_role"),
            models.Index(fields=["status"], name="idx_user_status"),
        ]

    def __str__(self):
        return self.username

    def bump_token_version(self):
        """递增 token 版本号并落库,使该用户历史 token 立即失效。

        登出、修改密码、管理员强制下线等场景调用本方法。
        """
        self.token_version += 1
        self.save(update_fields=["token_version", "updated_at"])
