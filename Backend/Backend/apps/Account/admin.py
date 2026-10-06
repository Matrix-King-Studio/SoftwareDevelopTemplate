from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from Account.models import User

# 修改网页 Title (浏览器标签页标题)
admin.site.site_title = "{{ProjectChineseName}} 管理平台"
# 修改登录页和首页页眉 (大的标题)
admin.site.site_header = "{{ProjectChineseName}} 管理平台"
# 修改首页标语 (首页中间标题)
admin.site.index_title = "{{ProjectChineseName}} 管理平台"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """自定义用户后台管理。

    在 Django 默认 UserAdmin 基础上,展示并支持编辑项目新增的
    role / status / token_version 字段。
    """

    list_display = ("id", "username", "email", "role", "status", "is_staff", "date_joined")
    list_filter = ("role", "status", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    # 在默认字段分组后追加业务字段分组
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("业务字段", {"fields": ("role", "status", "token_version", "avatar")}),
    )
