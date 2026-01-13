import os
import logging


# 自定义日志格式
def post_fork(server, worker):
    """在 worker 进程启动后配置日志格式"""

    # 确保日志目录存在
    log_dir = '/usr/local/var/log/django'
    log_file = os.path.join(log_dir, 'error.log')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    if not os.path.exists(log_file):
        open(log_file, 'a').close()

    # 1. 配置 Gunicorn 错误日志
    gunicorn_logger = logging.getLogger('gunicorn.error')
    gunicorn_logger.setLevel(logging.DEBUG)

    gunicorn_handler = logging.FileHandler(log_file)
    gunicorn_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    gunicorn_handler.setFormatter(gunicorn_formatter)
    gunicorn_logger.addHandler(gunicorn_handler)

    # 2. 配置 Django 应用错误日志
    django_logger = logging.getLogger('django')
    django_logger.setLevel(logging.DEBUG)

    django_handler = logging.FileHandler(log_file)
    django_handler.setLevel(logging.DEBUG)
    django_handler.setFormatter(gunicorn_formatter)
    django_logger.addHandler(django_handler)
