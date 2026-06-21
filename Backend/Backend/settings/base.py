"""
Django 项目基础配置(所有环境共用)。

环境切分:
- dev.py：本地开发,SQLite + 本地内存缓存(LocMemCache),开箱即跑
- test.py / prod.py：MySQL + Redis,从环境变量读取连接信息

认证方案:纯自定义 JWT(Bearer),见 Backend/utils/auth/。
统一响应:{code, message, data, requestId},见 Backend/utils/drf/。
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 添加导包路径(使 apps 下的应用可直接以应用名导入,如 import Account)
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "apps"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-$-coch(nitp3%ld7#ffdlqbi5gyy=t9jdq&0fs@w*a=qx1gn!n"

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://localhost:8000"]

# Application definition
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

# 指定自定义用户模型(必须在首次 migrate 前设置)
AUTH_USER_MODEL = "Account.User"

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

WSGI_APPLICATION = "Backend.wsgi_dev.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR.parent, "static")
os.makedirs(STATIC_ROOT, exist_ok=True)
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR.parent, "media")
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Default primary key field type
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
# 签名密钥默认回退到 SECRET_KEY;生产环境建议用环境变量单独配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_TTL_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_TTL_MINUTES", "30"))
JWT_REFRESH_TOKEN_TTL_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_TTL_DAYS", "7"))

# ═══════════════════════════════════════════════════════════════════════════════
# CORS 跨域
# ═══════════════════════════════════════════════════════════════════════════════
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
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

# SimpleUI
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_DEFAULT_ICON = False

# ═══════════════════════════════════════════════════════════════════════════════
# 日志
# ═══════════════════════════════════════════════════════════════════════════════
LOG_DIR = os.path.join(BASE_DIR.parent, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 成功请求日志的最小耗时阈值(毫秒):0=记录全部成功请求
REQUEST_LOG_SUCCESS_MIN_DURATION_MS = int(os.getenv("REQUEST_LOG_SUCCESS_MIN_DURATION_MS", "0"))

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
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["request_id"],
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "django.log"),
            "maxBytes": 300 * 1024 * 1024,
            "backupCount": 10,
            "formatter": "verbose",
            "encoding": "utf-8",
            "filters": ["request_id"],
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "maxBytes": 300 * 1024 * 1024,
            "backupCount": 10,
            "formatter": "verbose",
            "encoding": "utf-8",
            "filters": ["request_id"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
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
            "level": "INFO",
            "propagate": False,
        },
    },
}
