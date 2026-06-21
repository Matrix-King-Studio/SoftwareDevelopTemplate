"""
账户相关序列化器。

包含:
- ``RegisterSerializer``：注册参数校验(username/email/password1/password2)
- ``LoginSerializer``：登录参数校验(username/password)
- ``RefreshTokenSerializer``：刷新令牌参数校验(refresh_token)
- ``UserInfoSerializer``：用户信息输出(供前端展示与本地缓存)

字段契约与前端 ``Frontend/src/types/auth.ts`` 对应,改动需前后端同步。
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    """用户信息输出序列化器。

    对应前端 ``UserInfo`` 类型,登录/获取当前用户接口的 ``data.user`` 即此结构。
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "status", "avatar", "date_joined"]
        read_only_fields = fields


class RegisterSerializer(serializers.Serializer):
    """注册参数校验。

    前端注册表单提交 username / email / password1 / password2,
    此处完成格式校验、用户名唯一性校验与两次密码一致性校验。
    """

    username = serializers.CharField(max_length=150, help_text="用户名")
    email = serializers.EmailField(required=False, allow_blank=True, help_text="邮箱(可选)")
    password1 = serializers.CharField(min_length=6, write_only=True, help_text="密码,至少 6 位")
    password2 = serializers.CharField(write_only=True, help_text="确认密码")

    def validate_username(self, value):
        """用户名唯一性校验。"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被注册")
        return value

    def validate(self, attrs):
        """两次密码一致性校验。"""
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("两次输入的密码不一致")
        return attrs

    def create(self, validated_data):
        """创建用户(使用 set_password 哈希密码)。"""
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """登录参数校验(用户名 + 密码)。"""

    username = serializers.CharField(help_text="用户名")
    password = serializers.CharField(write_only=True, help_text="密码")


class RefreshTokenSerializer(serializers.Serializer):
    """刷新令牌参数校验。"""

    refresh_token = serializers.CharField(help_text="登录时返回的 refresh_token")
