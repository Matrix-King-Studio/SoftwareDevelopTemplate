python manage.py makemigrations --settings=Backend.settings.prod
python manage.py migrate --settings=Backend.settings.prod

# 在收集静态文件之前先删除静态文件夹，否则会询问是否覆盖导致报错
if [ -d "static" ]; then
  rm -rf static
fi
python manage.py collectstatic

# 如果有异步任务的话，需要把下面两行打开
# nohup celery -A Backend worker -l INFO --concurrency=1 > /usr/local/var/log/celery_worker.log 2>&1 &
# nohup celery -A Backend beat   -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler > /usr/local/var/log/celery_beat.log 2>&1 &

gunicorn --bind=0.0.0.0:8000 --capture-output --workers=1 --threads=1 --timeout 60 -c gunicorn_conf.py Backend.wsgi_prod:application
