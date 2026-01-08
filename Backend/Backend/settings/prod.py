import os

from pathlib import Path

from .base import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MYSQL_HOST = os.getenv("MYSQL_HOST", "39.101.***.131")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_NAME = os.getenv('MYSQL_NAME', "software-template-prod")
MYSQL_USER = os.getenv("MYSQL_USER", "software-template-prod")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "HyyNj*****Xc6ck")
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

REDIS_HOST = os.getenv("REDIS_HOST", "39.101.***.131")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "4"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "Matrix*****Redis")
