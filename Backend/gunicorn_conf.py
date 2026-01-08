import logging


# 自定义日志格式
def post_fork(server, worker):
    """在 worker 进程启动后配置日志格式"""
    
    # 1. 配置 Gunicorn 错误日志
    gunicorn_logger = logging.getLogger('gunicorn.error')
    gunicorn_logger.setLevel(logging.DEBUG)
    
    gunicorn_handler = logging.FileHandler('/usr/local/var/log/django/error.log')
    gunicorn_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    gunicorn_handler.setFormatter(gunicorn_formatter)
    gunicorn_logger.addHandler(gunicorn_handler)
    
    # 2. 配置 Django 应用错误日志
    django_logger = logging.getLogger('django')
    django_logger.setLevel(logging.DEBUG)
    
    django_handler = logging.FileHandler('/usr/local/var/log/django/error.log')
    django_handler.setLevel(logging.DEBUG)
    django_handler.setFormatter(gunicorn_formatter)
    django_logger.addHandler(django_handler) 
