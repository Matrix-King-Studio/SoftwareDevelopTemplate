# {{ProjectChineseName}} 后端

后端基于 Django + Django REST Framework，内置自定义用户模型、JWT Bearer 认证、统一响应、统一异常处理、请求日志、MySQL、Redis、Gunicorn 和 Docker Compose 部署配置。

这份后端代码拿到新项目后不能直接上线。需要先按本文完成项目命名、数据库、Redis、密钥、域名、跨域、部署脚本和 CI/CD 配置。

## 目录结构

```text
Backend/
├── Backend/
│   ├── apps/Account/          账号模型、序列化器、视图、路由、测试
│   ├── settings/              dev/test/prod/unittest 分环境配置
│   ├── utils/auth/            JWT、认证、权限
│   ├── utils/drf/             统一响应、分页、异常处理
│   ├── utils/log/             requestId 和请求日志
│   ├── urls.py
│   ├── wsgi_dev.py
│   ├── wsgi_test.py
│   └── wsgi_prod.py
├── .env.dev.example
├── .env.test.example
├── .env.prod.example
├── docker-compose-test.yml
├── docker-compose-prod.yml
├── django-entrypoint-test.sh
├── django-entrypoint-prod.sh
├── gunicorn_config.py
├── Makefile
└── requirements.txt
```

## 拿到模板后必须修改

### 0. 全局搜索替换

后端保留 `{{...}}` 占位符用于快速初始化。先按根目录 [README.md](../README.md) 的全局替换表处理以下关键 token：

- `{{ProjectChineseName}}`
- `{{DOCKER_NAMESPACE}}`
- `{{TEST_DJANGO_PORT}}` / `{{PROD_DJANGO_PORT}}`
- `{{DEV_MYSQL_NAME}}` / `{{TEST_MYSQL_NAME}}` / `{{PROD_MYSQL_NAME}}`
- `{{DEV_MYSQL_USER}}` / `{{TEST_MYSQL_USER}}` / `{{PROD_MYSQL_USER}}`
- `{{DEV_MYSQL_PASSWORD}}` / `{{TEST_MYSQL_PASSWORD}}` / `{{PROD_MYSQL_PASSWORD}}`
- `{{DEV_MYSQL_HOST}}` / `{{TEST_MYSQL_HOST}}` / `{{PROD_MYSQL_HOST}}`
- `{{DEV_REDIS_PASSWORD}}` / `{{TEST_REDIS_PASSWORD}}` / `{{PROD_REDIS_PASSWORD}}`
- `{{DEV_REDIS_HOST}}` / `{{TEST_REDIS_HOST}}` / `{{PROD_REDIS_HOST}}`
- `{{DEV_SECRET_KEY}}` / `{{TEST_SECRET_KEY}}` / `{{PROD_SECRET_KEY}}`
- `{{DEV_ALLOWED_HOSTS}}` / `{{TEST_ALLOWED_HOSTS}}` / `{{PROD_ALLOWED_HOSTS}}`
- `{{DEV_CSRF_TRUSTED_HOSTS}}` / `{{TEST_CSRF_TRUSTED_HOSTS}}` / `{{PROD_CSRF_TRUSTED_HOSTS}}`

### 1. 项目名称

需要修改的位置：

- `Backend/Backend/apps/Account/admin.py`：Django Admin 标题。
- `Backend/docker-compose-test.yml`：`name`、`image`、`container_name`、network。
- `Backend/docker-compose-prod.yml`：`name`、`image`、`container_name`、network。
- `.github/workflows/Backend.yml`：Docker 镜像 tag。
- 数据库名：`MYSQL_NAME`。
- Redis key 前缀：`REDIS_KEY_PREFIX`。

命名建议：

```text
项目英文名：smart-campus
镜像名：registry.cn-hangzhou.aliyuncs.com/matrix-studio/smart-campus
测试库：smart_campus_test
生产库：smart_campus_prod
Redis 前缀：smart-campus-test / smart-campus-prod
```

### 2. 环境变量文件

真实环境变量文件不提交 Git：

- `Backend/.env.dev`
- `Backend/.env.test`
- `Backend/.env.prod`

提交到 Git 的只有：

- `Backend/.env.dev.example`
- `Backend/.env.test.example`
- `Backend/.env.prod.example`

初始化新项目时可以复制：

```shell
cd Backend
cp .env.dev.example .env.dev
cp .env.test.example .env.test
cp .env.prod.example .env.prod
```

配置优先级：

1. 系统环境变量 / Docker Compose `environment`
2. `.env.<env>`
3. settings 代码里的默认值

Docker Compose 文件不使用 `env_file`，部署环境变量直接写在 `docker-compose-test.yml` / `docker-compose-prod.yml` 的 `environment` 中。

### 3. MySQL

三套真实运行环境 `dev` / `test` / `prod` 都使用 MySQL。

必须确认：

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_NAME`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

建议每个环境使用独立数据库：

```text
dev:  <project>_dev
test: <project>_test
prod: <project>_prod
```

不要让测试环境和生产环境共用数据库。不要把生产数据库密码写入代码或 README。

### 4. Redis

三套真实运行环境 `dev` / `test` / `prod` 都使用 Redis，配置由 `Backend/Backend/settings/base.py` 的 `build_redis_cache_config()` 统一封装。

必须确认：

- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_DB`
- `REDIS_PASSWORD`
- `REDIS_KEY_PREFIX`
- `REDIS_CACHE_TIMEOUT`
- `REDIS_SOCKET_CONNECT_TIMEOUT`
- `REDIS_SOCKET_TIMEOUT`

默认 DB 约定：

- `prod`: `0`
- `test`: `1`
- `dev`: `2`

如果多个项目共用 Redis，必须设置独立 `REDIS_KEY_PREFIX`。

### 5. Django 安全项

生产部署前必须修改：

- `SECRET_KEY`：使用独立随机值。
- `ALLOWED_HOSTS`：只保留实际域名/IP。
- `CSRF_TRUSTED_ORIGINS`：配置真实 HTTPS 来源。
- `CORS_ORIGIN_ALLOW_ALL`：生产建议为 `false`。
- `CORS_ALLOWED_ORIGINS`：配置前端真实域名。

示例：

```env
SECRET_KEY=<随机强密钥>
ALLOWED_HOSTS=api.example.com,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://api.example.com
CORS_ORIGIN_ALLOW_ALL=false
CORS_ALLOWED_ORIGINS=https://app.example.com
```

### 6. JWT

JWT 配置位于 `Backend/Backend/settings/base.py`：

- `JWT_SECRET_KEY`：默认回退到 `SECRET_KEY`，如需独立签名密钥可单独配置。
- `JWT_ACCESS_TOKEN_TTL_MINUTES`：access token 有效期。
- `JWT_REFRESH_TOKEN_TTL_DAYS`：refresh token 有效期。

当前认证接口：

| 接口 | 方法 | 说明 | 认证 |
| --- | --- | --- | --- |
| `/auth/registration/` | POST | 注册 | 公开 |
| `/auth/login/` | POST | 登录 | 公开 |
| `/auth/user/` | GET | 当前用户 | 需要 access token |
| `/auth/logout/` | POST | 登出并递增 token_version | 需要 access token |
| `/auth/token/refresh/` | POST | 刷新 access token | 公开 |

前端通过 `/api` 代理到后端时，请求路径为 `/api/auth/login/`，后端实际路由为 `/auth/login/`。

### 7. Gunicorn

只保留一个 `Backend/gunicorn_config.py`。入口脚本通过 `GUNICORN_ENV_NAME` 区分环境：

- `django-entrypoint-test.sh`: `GUNICORN_ENV_NAME=test`
- `django-entrypoint-prod.sh`: `GUNICORN_ENV_NAME=prod`

默认并发：

- test：`GUNICORN_WORKERS=1`、`GUNICORN_THREADS=1`
- prod：`GUNICORN_WORKERS=3`、`GUNICORN_THREADS=2`

可按服务器资源调整：

```env
GUNICORN_WORKERS=3
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=60
GUNICORN_LOG_LEVEL=info
```

日志写入：

- Django 日志：`/app/Backend/logs/django.log`
- Django 错误日志：`/app/Backend/logs/error.log`
- Gunicorn access log：`/app/Backend/logs/gunicorn-access.log`
- Gunicorn error log：`/app/Backend/logs/gunicorn-error.log`

Compose 默认挂载：

```yaml
./log:/app/Backend/logs
./media:/app/Backend/media
```

### 8. Docker Compose

测试环境：

```shell
cd Backend
make pull_test
make restart_test
```

生产环境：

```shell
cd Backend
make pull_prod
make restart_prod
```

新项目必须检查：

- 镜像仓库地址是否正确。
- 宿主机端口是否冲突。
- `container_name` 是否与其他项目冲突。
- network 名是否与其他项目冲突。
- `./log` 和 `./media` 目录权限是否正确。
- `MYSQL_HOST` / `REDIS_HOST` 在容器内是否可访问。

如果 MySQL/Redis 跑在宿主机，容器里的 `127.0.0.1` 指向容器自身，不是宿主机。需要改为宿主机内网 IP、Docker network service name，或 `host.docker.internal` 等可达地址。

### 9. GitHub Actions

后端部署工作流：`.github/workflows/Backend.yml`

必须修改：

- Docker 镜像 tag 中的项目英文名。
- 分支触发规则。
- 远程服务器部署路径。
- 镜像仓库登录方式。

必须配置 GitHub Secrets：

```text
ALI_DOCKER_USERNAME
ALI_DOCKER_PASSWORD
TEST_SSH_PRIVATE_KEY
TEST_REMOTE_HOST
TEST_REMOTE_USER
TEST_DEPLOY_TARGET
PROD_SSH_PRIVATE_KEY
PROD_REMOTE_HOST
PROD_REMOTE_USER
PROD_DEPLOY_TARGET
```

## 本地开发

```shell
cd Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.dev.example .env.dev
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

默认 settings：

```text
Backend.settings.dev
```

## 数据库迁移

新增或修改模型后：

```shell
python manage.py makemigrations
python manage.py migrate
```

提交代码时必须提交 migrations 文件。不要让服务器自动生成迁移文件后不回传仓库，否则多环境迁移历史会不一致。

自定义用户模型 `AUTH_USER_MODEL = "Account.User"` 必须在项目首次迁移前确定。已经迁移上线后，不要随意替换用户模型。

## 单元测试

自动化单元测试使用 `Backend.settings.unittest`：

- SQLite 内存数据库
- LocMemCache
- 不连接 MySQL
- 不连接 Redis

运行：

```shell
make test
```

## 质量检查

```shell
make lint
make format-check
python manage.py check --settings=Backend.settings.dev
python manage.py check --settings=Backend.settings.test
python manage.py check --settings=Backend.settings.prod
python manage.py check --settings=Backend.settings.unittest
```

## 新增业务应用

应用统一放在 `Backend/Backend/apps/` 下。

```shell
cd Backend/Backend/apps
python ../../manage.py startapp ApplicationName
```

新增后需要：

- 在 `Backend/Backend/settings/base.py` 的 `INSTALLED_APPS` 添加应用。
- 添加 `urls.py` 并接入 `Backend/Backend/urls.py`。
- 为模型生成 migrations。
- 添加 API 测试。

## 接口响应规范

统一响应格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "requestId": "uuid"
}
```

`requestId` 会同时写入响应头 `X-Request-Id`，并进入日志，便于前后端排查同一次请求。

## 上线前检查清单

- `DEBUG=False`。
- `SECRET_KEY` 已替换为强随机值。
- `ALLOWED_HOSTS` 已收紧。
- `CORS_ORIGIN_ALLOW_ALL=false`。
- `CORS_ALLOWED_ORIGINS` 是真实前端域名。
- MySQL/Redis 使用生产实例。
- 生产数据库密码未提交到 Git。
- 生产 `.env.prod` 未提交到 Git。
- Gunicorn worker/thread 符合服务器资源。
- 日志目录和 media 目录已经挂载。
- `make lint` 通过。
- `make format-check` 通过。
- `make test` 通过。
- `python manage.py check --settings=Backend.settings.prod` 通过。
