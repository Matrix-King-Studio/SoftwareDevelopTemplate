import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

MYSQL_HOST = os.getenv("MYSQL_HOST", "prod_mysql_host")
MYSQL_PORT = os.getenv("MYSQL_PORT", "prod_mysql_port")
MYSQL_NAME = os.getenv('MYSQL_NAME', "prod_mysql_name")
MYSQL_USER = os.getenv("MYSQL_USER", "prod_mysql_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "prod_mysql_password")
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

REDIS_HOST = os.getenv("REDIS_HOST", "prod_redis_host")
REDIS_PORT = int(os.getenv("REDIS_PORT", "prod_redis_port"))
REDIS_DB = int(os.getenv("REDIS_DB", "prod_redis_db"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "prod_redis_password")
