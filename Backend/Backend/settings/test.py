import os

from pathlib import Path

from .base import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MYSQL_HOST = os.getenv("MYSQL_HOST", "test_mysql_host")
MYSQL_PORT = os.getenv("MYSQL_PORT", "test_mysql_port")
MYSQL_NAME = os.getenv('MYSQL_NAME', "test_mysql_name")
MYSQL_USER = os.getenv("MYSQL_USER", "test_mysql_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "test_mysql_password")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_NAME,
        "HOST": MYSQL_HOST,
        "PORT": MYSQL_PORT,
        "PASSWORD": MYSQL_PASSWORD,
        "USER": MYSQL_USER
    }
}

REDIS_HOST = os.getenv("REDIS_HOST", "test_redis_host")
REDIS_PORT = int(os.getenv("REDIS_PORT", "test_redis_port"))
REDIS_DB = int(os.getenv("REDIS_DB", "test_redis_db"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "test_redis_password")
