import os
from pathlib import Path


def load_env_file():
    """在 Gunicorn 读取配置前加载对应环境变量文件。

    Django settings 会在导入 ``Backend.settings.test/prod`` 时加载 ``.env.test`` 或
    ``.env.prod``。但 Gunicorn 会先读取本文件,此时 Django settings 尚未执行,因此这里
    需要独立加载一次环境变量文件,确保 ``GUNICORN_WORKERS`` / ``GUNICORN_THREADS`` 等
    Gunicorn 自身参数也能从环境变量文件生效。

    优先级:
    1. 系统环境变量或 docker-compose ``environment`` 中显式传入的值;
    2. ``Backend/.env.test`` 或 ``Backend/.env.prod`` 中的值;
    3. 本文件里的代码默认值。

    本函数不会覆盖已经存在的系统环境变量,避免部署平台注入的真实配置被本地文件覆盖。
    """
    env_name = os.getenv("GUNICORN_ENV_NAME", "prod")
    env_file = Path(__file__).resolve().parent / f".env.{env_name}"
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


def env_int(name, default):
    raw = os.getenv(name, str(default))
    try:
        return int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be an integer, got {raw!r}") from exc


def env_bool(name, default=False):
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def default_workers():
    """返回当前环境的默认 worker 进程数。

    测试环境默认 1 个 worker,便于排查问题、减少测试机资源占用,并避免多进程导致日志顺序
    更难阅读。生产环境默认 3 个 worker,在不额外配置的情况下提供基础并发能力和进程隔离。
    如果部署机器资源更高或更低,可通过 ``GUNICORN_WORKERS`` 覆盖。
    """
    return 1 if os.getenv("GUNICORN_ENV_NAME", "prod") == "test" else 3


def default_threads():
    """返回当前环境的默认每 worker 线程数。

    测试环境默认 1 个线程,保持行为更可预测。生产环境默认 2 个线程,让同步 worker 在遇到
    轻量 I/O 等待时具备基本并发能力。若业务请求主要是 CPU 密集型,应谨慎增大线程数。
    """
    return 1 if os.getenv("GUNICORN_ENV_NAME", "prod") == "test" else 2


# 日志目录固定放在 Backend/logs 下。docker-compose 会把宿主机 ./log 挂载到
# 容器内 /app/Backend/logs,因此 Django 日志和 Gunicorn 日志最终都能落到同一宿主机目录。
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 网络监听地址。默认监听容器内 0.0.0.0:8000,由 docker-compose 的 ports 映射到宿主机端口。
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")

# 并发配置。优先读取环境变量文件或 compose environment;未配置时按 test/prod 给默认值。
workers = env_int("GUNICORN_WORKERS", default_workers())
threads = env_int("GUNICORN_THREADS", default_threads())

# worker 类型。当前项目是普通 Django WSGI 应用,默认使用 sync worker。
# 如后续引入 gevent/eventlet 等异步 worker,需要同步确认依赖、数据库连接和中间件兼容性。
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "sync")

# 请求超时配置:
# - timeout: 单个请求超过该秒数未响应时,worker 会被 Gunicorn 重启;
# - graceful_timeout: 优雅重启时等待 worker 退出的最长时间;
# - keepalive: HTTP keep-alive 连接保持时间。
timeout = env_int("GUNICORN_TIMEOUT", 60)
graceful_timeout = env_int("GUNICORN_GRACEFUL_TIMEOUT", 30)
keepalive = env_int("GUNICORN_KEEPALIVE", 2)

# 捕获 stdout/stderr 后写入 Gunicorn errorlog,便于容器部署时集中排查启动和运行错误。
capture_output = env_bool("GUNICORN_CAPTURE_OUTPUT", True)

# worker 临时目录。Linux 容器里使用 /dev/shm 可减少磁盘 I/O;若运行环境没有该目录,
# 可通过 GUNICORN_WORKER_TMP_DIR 覆盖。
worker_tmp_dir = os.getenv("GUNICORN_WORKER_TMP_DIR", "/dev/shm")

# Gunicorn 访问日志与错误日志。Django 应用日志由 settings/base.py 的 LOGGING 管理。
accesslog = str(LOG_DIR / "gunicorn-access.log")
errorlog = str(LOG_DIR / "gunicorn-error.log")
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

# worker 请求数回收策略。默认关闭(0),保持行为稳定。
# 如果后续发现第三方库存在内存泄漏,可设置 GUNICORN_MAX_REQUESTS 和抖动值
# GUNICORN_MAX_REQUESTS_JITTER,让 worker 在处理一定数量请求后自动重启。
max_requests = env_int("GUNICORN_MAX_REQUESTS", 0)
max_requests_jitter = env_int("GUNICORN_MAX_REQUESTS_JITTER", 0)
