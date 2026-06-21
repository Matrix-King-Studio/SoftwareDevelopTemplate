from .base import *  # noqa: F403

# 开发环境允许开启 DEBUG,便于本地查看错误堆栈和调试信息。
DEBUG = True
# 开发环境 WSGI 入口。runserver 主要使用 settings,但保持 WSGI 配置一致。
WSGI_APPLICATION = "Backend.wsgi_dev.application"

# 日志配置。开发环境默认 DEBUG,并记录所有成功请求。
DJANGO_LOG_LEVEL = env_str("DJANGO_LOG_LEVEL", "DEBUG")
REQUEST_LOG_LEVEL = env_str("REQUEST_LOG_LEVEL", DJANGO_LOG_LEVEL)
REQUEST_LOG_SUCCESS_MIN_DURATION_MS = env_int("REQUEST_LOG_SUCCESS_MIN_DURATION_MS", 0)
configure_logging(DJANGO_LOG_LEVEL, REQUEST_LOG_LEVEL)

# ── MySQL: 环境变量优先,缺省时使用开发占位值 ──
# 部署/本地可通过系统环境变量或 Backend/.env.dev 覆盖这些值。
MYSQL_HOST = env_str("MYSQL_HOST", "dev_mysql_host")
MYSQL_PORT = env_str("MYSQL_PORT", "3306")
MYSQL_NAME = env_str("MYSQL_NAME", "dev_mysql_name")
MYSQL_USER = env_str("MYSQL_USER", "dev_mysql_user")
MYSQL_PASSWORD = env_str("MYSQL_PASSWORD", "dev_mysql_password")
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

# ── Redis: 统一由 base.build_redis_cache_config 封装 ──
# 开发环境默认使用 REDIS_DB=2,避免和 test/prod 默认库冲突。
REDIS_HOST = env_str("REDIS_HOST", "dev_redis_host")
REDIS_PORT = env_int("REDIS_PORT", 6379)
REDIS_DB = env_int("REDIS_DB", 2)
REDIS_PASSWORD = env_str("REDIS_PASSWORD", "dev_redis_password")
REDIS_KEY_PREFIX = env_str("REDIS_KEY_PREFIX", "dev")
CACHES = build_redis_cache_config(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    key_prefix=REDIS_KEY_PREFIX,
    timeout=env_int("REDIS_CACHE_TIMEOUT", 300),
    socket_connect_timeout=env_int("REDIS_SOCKET_CONNECT_TIMEOUT", 5),
    socket_timeout=env_int("REDIS_SOCKET_TIMEOUT", 5),
)
