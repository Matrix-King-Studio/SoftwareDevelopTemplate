import os

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ── MySQL ──
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_NAME = os.getenv("MYSQL_NAME", "test_db")
MYSQL_USER = os.getenv("MYSQL_USER", "test_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "test_password")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_NAME,
        "HOST": MYSQL_HOST,
        "PORT": MYSQL_PORT,
        "PASSWORD": MYSQL_PASSWORD,
        "USER": MYSQL_USER,
    }
}

# ── Redis ──
# 注意:端口/库号必须是合法整数,默认值给数字字符串避免 int() 转换崩溃
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

_redis_auth = f":{REDIS_PASSWORD}@" if REDIS_PASSWORD else ""
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{_redis_auth}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}
