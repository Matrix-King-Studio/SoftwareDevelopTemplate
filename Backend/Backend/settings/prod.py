from .base import *

# 生产环境必须关闭 DEBUG,避免向用户暴露错误堆栈、settings 和环境信息。
DEBUG = False
# 生产环境 WSGI 入口,由 django-entrypoint-prod.sh 的 Gunicorn 命令使用。
WSGI_APPLICATION = "Backend.wsgi_prod.application"

# 日志配置。生产环境默认 INFO,且只记录慢成功请求。
DJANGO_LOG_LEVEL = env_str("DJANGO_LOG_LEVEL", "INFO")
REQUEST_LOG_LEVEL = env_str("REQUEST_LOG_LEVEL", DJANGO_LOG_LEVEL)
REQUEST_LOG_SUCCESS_MIN_DURATION_MS = env_int("REQUEST_LOG_SUCCESS_MIN_DURATION_MS", 1000)
configure_logging(DJANGO_LOG_LEVEL, REQUEST_LOG_LEVEL)

# ── MySQL: 环境变量优先,缺省时使用生产占位值 ──
# 实际部署时应在 docker-compose-prod.yml 的 environment 中替换 prod_mysql_*。
MYSQL_HOST = env_str("MYSQL_HOST", "prod_mysql_host")
MYSQL_PORT = env_str("MYSQL_PORT", "3306")
MYSQL_NAME = env_str("MYSQL_NAME", "prod_mysql_name")
MYSQL_USER = env_str("MYSQL_USER", "prod_mysql_user")
MYSQL_PASSWORD = env_str("MYSQL_PASSWORD", "prod_mysql_password")
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
# 生产环境默认使用 REDIS_DB=0。
REDIS_HOST = env_str("REDIS_HOST", "prod_redis_host")
REDIS_PORT = env_int("REDIS_PORT", 6379)
REDIS_DB = env_int("REDIS_DB", 0)
REDIS_PASSWORD = env_str("REDIS_PASSWORD", "prod_redis_password")
REDIS_KEY_PREFIX = env_str("REDIS_KEY_PREFIX", "prod")
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

# 生产安全建议(按需启用)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
