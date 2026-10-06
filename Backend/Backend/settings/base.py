"""
Django 项目基础配置(所有环境共用)。

环境切分:
- dev.py：本地开发环境,MySQL + Redis,从环境变量或 .env.dev 读取连接信息
- test.py：测试环境,MySQL + Redis,从环境变量或 .env.test 读取连接信息
- prod.py：生产环境,MySQL + Redis,从环境变量或 .env.prod 读取连接信息
- unittest.py：自动化单测环境,内存 SQLite + LocMemCache,不依赖外部服务

认证方案:纯自定义 JWT(Bearer),见 Backend/utils/auth/。
统一响应:{code, message, data, requestId},见 Backend/utils/drf/。
"""

import os
import sys
from pathlib import Path
from urllib.parse import quote

from django.core.exceptions import ImproperlyConfigured

# 项目路径:
# - 本文件位于 Backend/Backend/settings/base.py
# - BASE_DIR 指向 Backend/Backend
# - BASE_DIR.parent 指向 Backend,用于 logs/static/media 等项目级目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 添加导包路径(使 apps 下的应用可直接以应用名导入,如 import Account)
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "apps"))


def load_env_file():
    """加载当前 settings 对应的环境变量文件。

    例如:
    - ``Backend.settings.dev`` 读取 ``Backend/.env.dev``
    - ``Backend.settings.test`` 读取 ``Backend/.env.test``
    - ``Backend.settings.prod`` 读取 ``Backend/.env.prod``

    优先级:
    1. 系统环境变量 / docker-compose environment 中已经存在的值;
    2. ``.env.<env>`` 文件中的值;
    3. settings 代码里的默认值,例如 ``env_str("MYSQL_HOST", "127.0.0.1")``。

    这里不会覆盖已经存在的系统环境变量,避免部署平台注入的真实配置被本地文件覆盖。
    """
    env_name = os.getenv("DJANGO_SETTINGS_MODULE", "Backend.settings.dev").rsplit(".", 1)[-1]
    env_file = BASE_DIR.parent / f".env.{env_name}"
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


load_env_file()


def env_str(name, default):
    """读取字符串环境变量;不存在时返回代码默认值。"""
    return os.getenv(name, default)


def env_int(name, default):
    """读取整数环境变量;格式错误时抛出 Django 配置异常,让启动尽早失败。"""
    raw = os.getenv(name, str(default))
    try:
        return int(raw)
    except (TypeError, ValueError) as exc:
        raise ImproperlyConfigured(f"{name} must be an integer, got {raw!r}") from exc


def env_bool(name, default):
    """读取布尔环境变量;只接受明确的 true/false 写法,避免误配置被静默吞掉。"""
    raw = os.getenv(name)
    if raw is None:
        return default

    normalized = raw.strip().lower()
    if normalized in ("1", "true", "yes", "on"):
        return True
    if normalized in ("0", "false", "no", "off"):
        return False
    raise ImproperlyConfigured(f"{name} must be a boolean, got {raw!r}")


def env_list(name, default, separator=","):
    """读取逗号分隔的列表环境变量;空字符串会得到空列表。"""
    raw = os.getenv(name)
    if raw is None:
        return default
    return [item.strip() for item in raw.split(separator) if item.strip()]


def build_redis_cache_config(
    *,
    host,
    port,
    db,
    password="",
    key_prefix,
    timeout=300,
    socket_connect_timeout=5,
    socket_timeout=5,
):
    """构建 django-redis 缓存配置。

    dev/test/prod 三个真实环境都使用 Redis 缓存。各环境只负责传入 host/port/db/password
    等参数,Redis URL、连接超时、key 前缀等结构统一在这里生成,避免三份 settings 重复拼接。
    """
    redis_auth = f":{quote(str(password), safe='')}@" if password else ""
    redis_url = f"redis://{redis_auth}{host}:{port}/{db}"

    return {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_url,
            "KEY_PREFIX": key_prefix,
            "TIMEOUT": timeout,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SOCKET_CONNECT_TIMEOUT": socket_connect_timeout,
                "SOCKET_TIMEOUT": socket_timeout,
            },
        }
    }


# Django 签名密钥。系统环境变量或 .env.<env> 中的 SECRET_KEY 优先。
SECRET_KEY = env_str(
    "SECRET_KEY",
    "django-insecure-$-coch(nitp3%ld7#ffdlqbi5gyy=t9jdq&0fs@w*a=qx1gn!n",
)

# 允许访问的主机。生产环境应通过 ALLOWED_HOSTS 收紧为域名/IP 白名单。
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])

# 允许通过 HTTPS 访问后端时提交 CSRF 请求的来源。当前项目关闭了 CsrfViewMiddleware,
# 但保留该项便于后续启用 CSRF 防护。
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", ["https://localhost:8000"])

# 应用列表:
# - Django 内置应用提供 admin/auth/session/static 等能力
# - 第三方应用提供 DRF、过滤、跨域、Swagger、导入导出和 SimpleUI
# - 自定义业务应用统一放在 Backend/apps 下
INSTALLED_APPS = [
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_yasg",
    "import_export",
    # 自定义应用
    "Account",
]

# 指定自定义用户模型。该配置必须在首次 migrate 前确定,后续不可随意改动。
AUTH_USER_MODEL = "Account.User"

# 中间件链路。顺序会影响请求处理:
# - corsheaders 尽量靠前处理跨域头
# - AuthenticationMiddleware 之后才能在 RequestLogMiddleware 中读取 request.user
# - 当前项目关闭 CsrfViewMiddleware,API 主要依赖 Bearer JWT 鉴权
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 请求日志 + requestId 注入(置于 AuthenticationMiddleware 之后以获取 request.user)
    "Backend.utils.log.middleware.RequestLogMiddleware",
]

ROOT_URLCONF = "Backend.urls"

# Django 模板引擎配置。后台管理和部分 Django 组件依赖 DjangoTemplates。
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 默认 WSGI 入口。各环境 settings 会覆盖为对应的 wsgi_dev/test/prod。
WSGI_APPLICATION = "Backend.wsgi_dev.application"

# 密码校验规则。用于创建用户、修改密码等场景。
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 国际化与时区。USE_TZ=False 表示数据库中使用本地时间,需和项目时间处理约定保持一致。
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = False

# 静态文件和媒体文件目录。collectstatic 会收集到 STATIC_ROOT。
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR.parent, "static")
os.makedirs(STATIC_ROOT, exist_ok=True)
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR.parent, "media")
os.makedirs(MEDIA_ROOT, exist_ok=True)

# 默认主键类型。新模型未显式声明主键时使用 BigAutoField。
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ═══════════════════════════════════════════════════════════════════════════════
# DRF 配置
# ═══════════════════════════════════════════════════════════════════════════════
REST_FRAMEWORK = {
    # 自定义 JWT Bearer 认证(替代默认 Session / Token 认证)
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "Backend.utils.auth.authentication.BearerTokenAuthentication",
    ],
    # 默认要求登录,匿名接口用 permission_classes=[AllowAny] 显式开放
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # 全局异常处理器:统一 {code, message, data, requestId} 错误响应
    "EXCEPTION_HANDLER": "Backend.utils.drf.exception_handler.custom_exception_handler",
    # 统一分页
    "DEFAULT_PAGINATION_CLASS": "Backend.utils.drf.pagination.StandardPageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    # 登录接口限流(配合视图 throttle_scope="login")
    "DEFAULT_THROTTLE_RATES": {
        "login": "10/min",
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# JWT 配置(被 Backend/utils/auth/token_service.py 读取)
# ═══════════════════════════════════════════════════════════════════════════════
# JWT 签名密钥默认回退到 SECRET_KEY。真实项目建议在环境变量中配置独立密钥。
JWT_SECRET_KEY = env_str("JWT_SECRET_KEY", SECRET_KEY)
# JWT 签名算法。当前 TokenService 使用 HS256 对称签名。
JWT_ALGORITHM = "HS256"
# access token 有效期(分钟),用于普通接口鉴权。
JWT_ACCESS_TOKEN_TTL_MINUTES = env_int("JWT_ACCESS_TOKEN_TTL_MINUTES", 30)
# refresh token 有效期(天),用于刷新 access token。
JWT_REFRESH_TOKEN_TTL_DAYS = env_int("JWT_REFRESH_TOKEN_TTL_DAYS", 7)

# ═══════════════════════════════════════════════════════════════════════════════
# CORS 跨域
# ═══════════════════════════════════════════════════════════════════════════════
# CORS_ALLOW_CREDENTIALS=True 允许跨域请求携带凭证。
CORS_ALLOW_CREDENTIALS = env_bool("CORS_ALLOW_CREDENTIALS", True)
# CORS_ORIGIN_ALLOW_ALL=True 会放开所有来源;生产环境建议设置为 false 并配置白名单。
CORS_ORIGIN_ALLOW_ALL = env_bool("CORS_ORIGIN_ALLOW_ALL", True)
# CORS_ALLOWED_ORIGINS 用于生产白名单,多个来源用英文逗号分隔。
CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS", [])
CORS_ALLOW_METHODS = ("GET", "OPTIONS", "PATCH", "DELETE", "POST", "PUT", "VIEW")
CORS_ALLOW_HEADERS = (
    "XMLHttpRequest",
    "X_FILENAME",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-trace-id",
    "Pragma",
)

# SimpleUI 后台界面配置。关闭首页信息、分析和默认图标,保持后台更简洁。
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_DEFAULT_ICON = False

# ═══════════════════════════════════════════════════════════════════════════════
# 日志
# ═══════════════════════════════════════════════════════════════════════════════
# Django 通用日志级别。dev/test/prod 可通过 .env 或 compose environment 覆盖。
DJANGO_LOG_LEVEL = env_str("DJANGO_LOG_LEVEL", "INFO").upper()
# 请求日志 logger 的级别;默认跟随 DJANGO_LOG_LEVEL。
REQUEST_LOG_LEVEL = env_str("REQUEST_LOG_LEVEL", DJANGO_LOG_LEVEL).upper()
# 单个日志文件最大大小,默认 300MB。
DJANGO_LOG_MAX_BYTES = env_int("DJANGO_LOG_MAX_BYTES", 300 * 1024 * 1024)
# 日志轮转保留文件数量,默认保留 10 个历史文件。
DJANGO_LOG_BACKUP_COUNT = env_int("DJANGO_LOG_BACKUP_COUNT", 10)

# 日志目录固定在 Backend/logs。docker-compose 会把宿主机 ./log 挂载到该目录。
LOG_DIR = os.path.join(BASE_DIR.parent, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 成功请求日志的最小耗时阈值(毫秒):0=记录全部成功请求
REQUEST_LOG_SUCCESS_MIN_DURATION_MS = env_int("REQUEST_LOG_SUCCESS_MIN_DURATION_MS", 0)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # 过滤器:为每条日志注入 request_id(与响应体 requestId / 响应头 X-Request-Id 一致)
    "filters": {
        "request_id": {
            "()": "Backend.utils.log.request_id.RequestIDFilter",
        },
    },
    "formatters": {
        # 所有格式串都带 [rid:%(request_id)s],便于按 requestId 检索全链路日志
        "verbose": {
            "format": "%(levelname)s %(asctime)s [rid:%(request_id)s] "
            "%(module)s %(filename)s:%(lineno)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(asctime)s [rid:%(request_id)s] %(message)s"},
    },
    "handlers": {
        "console": {
            "level": DJANGO_LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["request_id"],
        },
        "file": {
            "level": DJANGO_LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "django.log"),
            "maxBytes": DJANGO_LOG_MAX_BYTES,
            "backupCount": DJANGO_LOG_BACKUP_COUNT,
            "formatter": "verbose",
            "encoding": "utf-8",
            "filters": ["request_id"],
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "maxBytes": DJANGO_LOG_MAX_BYTES,
            "backupCount": DJANGO_LOG_BACKUP_COUNT,
            "formatter": "verbose",
            "encoding": "utf-8",
            "filters": ["request_id"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "error_file"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": True,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        # 请求日志中间件专用 logger
        "request": {
            "handlers": ["console", "file", "error_file"],
            "level": REQUEST_LOG_LEVEL,
            "propagate": False,
        },
    },
}


def configure_logging(django_level, request_level=None):
    """让环境 settings 覆盖 base.py 中已经构造好的 LOGGING 级别。

    LOGGING 字典在 base.py 导入时已经创建。dev/test/prod 重新设置 ``DJANGO_LOG_LEVEL`` 后,
    需要调用本函数把 handler/logger 的 level 同步更新,否则 LOGGING 仍会保留 base.py 的默认值。
    """
    django_level = django_level.upper()
    request_level = (request_level or django_level).upper()

    LOGGING["handlers"]["console"]["level"] = django_level
    LOGGING["handlers"]["file"]["level"] = django_level
    LOGGING["loggers"]["django"]["level"] = django_level
    LOGGING["loggers"]["request"]["level"] = request_level
