from .base import *  # noqa: F403

# 测试环境保留 DEBUG=True,方便测试部署排查接口错误。
DEBUG = True
# 测试环境 WSGI 入口,由 django-entrypoint-test.sh 的 Gunicorn 命令使用。
WSGI_APPLICATION = "Backend.wsgi_test.application"

# 日志配置。测试环境默认 INFO,并记录所有成功请求。
DJANGO_LOG_LEVEL = env_str("DJANGO_LOG_LEVEL", "INFO")
REQUEST_LOG_LEVEL = env_str("REQUEST_LOG_LEVEL", DJANGO_LOG_LEVEL)
REQUEST_LOG_SUCCESS_MIN_DURATION_MS = env_int("REQUEST_LOG_SUCCESS_MIN_DURATION_MS", 0)
configure_logging(DJANGO_LOG_LEVEL, REQUEST_LOG_LEVEL)

# ── MySQL: 环境变量优先,缺省时使用测试占位值 ──
# 实际部署时应在 docker-compose-test.yml 的 environment 中替换 test_mysql_*。
MYSQL_HOST = env_str("MYSQL_HOST", "test_mysql_host")
MYSQL_PORT = env_str("MYSQL_PORT", "3306")
MYSQL_NAME = env_str("MYSQL_NAME", "test_mysql_name")
MYSQL_USER = env_str("MYSQL_USER", "test_mysql_user")
MYSQL_PASSWORD = env_str("MYSQL_PASSWORD", "test_mysql_password")
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
# 测试环境默认使用 REDIS_DB=1,避免和生产默认 DB=0 冲突。
REDIS_HOST = env_str("REDIS_HOST", "test_redis_host")
REDIS_PORT = env_int("REDIS_PORT", 6379)
REDIS_DB = env_int("REDIS_DB", 1)
REDIS_PASSWORD = env_str("REDIS_PASSWORD", "test_redis_password")
REDIS_KEY_PREFIX = env_str("REDIS_KEY_PREFIX", "test")
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
