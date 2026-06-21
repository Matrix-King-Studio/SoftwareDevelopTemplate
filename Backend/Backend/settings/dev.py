from pathlib import Path

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 本地开发使用 SQLite,无需额外数据库服务
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 本地开发使用进程内存缓存:不依赖 Redis 即可开箱运行。
# 如需本地联调 Redis,可将下方替换为 test.py / prod.py 中的 django_redis 配置。
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "dev-default-cache",
    }
}
