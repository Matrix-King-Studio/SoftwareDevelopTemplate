"""
自动化测试专用 Django settings。

用途:
1. 供 ``python manage.py test --settings=Backend.settings.unittest`` 使用;
2. 与 dev / test / prod 三套真实环境的数据库、缓存完全隔离;
3. 使用内存 SQLite + 本地内存缓存,不连接任何 MySQL / Redis 实例,
   即使本机未启动数据库/缓存服务也能跑单测。
"""

from .base import *  # noqa: F403

DEBUG = True

# ── 内存 SQLite:测试结束即销毁,不落任何文件,不碰 MySQL ──
# 单元测试只验证业务逻辑和 API 行为,不依赖外部数据库服务。
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# ── 本地进程内存缓存:不依赖 Redis ──
# 避免单测环境因为 Redis 未启动而失败。
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unittest-default",
    }
}

# ── 加速密码哈希:单测中大量建用户时显著提速(仅测试环境可用此弱哈希) ──
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# ── 邮件走内存后端,不真正发信 ──
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# ── 静默日志:避免测试输出被请求日志/错误日志刷屏 ──
# 覆盖 base.py 的 LOGGING(不加载 RequestIDFilter),仅保留 CRITICAL 级别。
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "CRITICAL",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "CRITICAL",
    },
}
