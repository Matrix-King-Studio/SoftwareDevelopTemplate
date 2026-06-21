#!/bin/sh
set -eu

export GUNICORN_ENV_NAME=test

python manage.py migrate --settings=Backend.settings.test

# 在收集静态文件之前先删除静态文件夹，否则会询问是否覆盖导致报错
if [ -d "static" ]; then
  rm -rf static
fi
python manage.py collectstatic --noinput --settings=Backend.settings.test

# 如果有异步任务的话，需要把下面两行打开
# nohup celery -A Backend worker -l INFO --concurrency=1 > logs/celery_worker.log 2>&1 &
# nohup celery -A Backend beat   -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler > logs/celery_beat.log 2>&1 &

gunicorn -c gunicorn_config.py Backend.wsgi_test:application
