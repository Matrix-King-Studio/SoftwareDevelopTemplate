# {{ProjectChineseName}}

这是一个前后端分离项目骨架，包含 `Backend` Django 后端、`Frontend` Vue 3 前端、GitHub Actions 部署流程、代码质量检查和基础账号体系。

拿到这份工程后，不要只改业务代码。需要先完成项目命名、环境变量、部署目标、数据库、Redis、域名、CI/CD secrets 和页面内容的初始化，否则默认配置只能作为本地骨架使用。

## 拿到模板后先改什么

### 0. 先做全局搜索替换

项目里保留了 `{{...}}` 形式的占位符，便于新项目初始化时一次性全局搜索替换。建议先按下表替换，再继续改业务代码。

| 全局搜索 | 替换为 |
| --- | --- |
| `{{ProjectChineseName}}` | 项目中文名，例如 `智慧校园` |
| `{{DOCKER_NAMESPACE}}` | 项目英文名 / Docker 镜像名，例如 `smart-campus` |
| `{{FRONTEND_PACKAGE_NAME}}` | 前端 package 名，例如 `smart-campus-frontend` |
| `{{TEST_DJANGO_PORT}}` | 测试环境后端宿主机端口，例如 `18080` |
| `{{PROD_DJANGO_PORT}}` | 生产环境后端宿主机端口，例如 `8000` |
| `{{DEV_MYSQL_NAME}}` | 开发库名，例如 `smart_campus_dev` |
| `{{TEST_MYSQL_NAME}}` | 测试库名，例如 `smart_campus_test` |
| `{{PROD_MYSQL_NAME}}` | 生产库名，例如 `smart_campus_prod` |
| `{{DEV_MYSQL_USER}}` / `{{TEST_MYSQL_USER}}` / `{{PROD_MYSQL_USER}}` | 各环境 MySQL 用户名 |
| `{{DEV_MYSQL_PASSWORD}}` / `{{TEST_MYSQL_PASSWORD}}` / `{{PROD_MYSQL_PASSWORD}}` | 各环境 MySQL 密码 |
| `{{DEV_MYSQL_HOST}}` / `{{TEST_MYSQL_HOST}}` / `{{PROD_MYSQL_HOST}}` | 各环境 MySQL 地址 |
| `{{DEV_REDIS_PASSWORD}}` / `{{TEST_REDIS_PASSWORD}}` / `{{PROD_REDIS_PASSWORD}}` | 各环境 Redis 密码，无密码时可替换为空 |
| `{{DEV_REDIS_HOST}}` / `{{TEST_REDIS_HOST}}` / `{{PROD_REDIS_HOST}}` | 各环境 Redis 地址 |
| `{{DEV_SECRET_KEY}}` / `{{TEST_SECRET_KEY}}` / `{{PROD_SECRET_KEY}}` | 各环境 Django `SECRET_KEY` |
| `{{DEV_ALLOWED_HOSTS}}` / `{{TEST_ALLOWED_HOSTS}}` / `{{PROD_ALLOWED_HOSTS}}` | Django Host 白名单，例如 `api.test.example.com,127.0.0.1` |
| `{{DEV_CSRF_TRUSTED_HOSTS}}` / `{{TEST_CSRF_TRUSTED_HOSTS}}` / `{{PROD_CSRF_TRUSTED_HOSTS}}` | CSRF 可信来源 host，例如 `api.example.com`，文件里已带 `https://` |
| `{{TEST_FRONTEND_API_BASE_URL}}` / `{{PROD_FRONTEND_API_BASE_URL}}` | 前端请求后端地址，例如 `/api` 或 `https://api.example.com` |

替换完成后再运行：

```shell
rg "\{\{"
```

如果还有残留，说明还有占位符没有处理完。

### 1. 项目命名

需要统一修改以下内容：

- 仓库名称：改成真实项目英文名，建议小写短横线，例如 `smart-campus`。
- 根 README 标题：替换 `{{ProjectChineseName}}`。
- 后端 Docker 镜像名：替换 `{{DOCKER_NAMESPACE}}`。
- Docker Compose `name`、`container_name`、network 名：避免同一服务器多个项目冲突。
- 后端 Django Admin 标题：`Backend/Backend/apps/Account/admin.py`。
- 前端应用标题：`Frontend/.env.development`、`Frontend/.env.test`、`Frontend/.env.prod` 的 `VITE_APP_TITLE`。
- 前端首页文案：`Frontend/src/views/Index.vue`。

命名建议：

```text
项目中文名：智慧校园
项目英文名：smart-campus
Docker 镜像：registry.cn-hangzhou.aliyuncs.com/matrix-studio/smart-campus
数据库：smart_campus_dev / smart_campus_test / smart_campus_prod
容器名：smart-campus-django
网络名：smart-campus-net
```

### 2. 环境和分支

默认分支约定：

- `master`：生产环境分支，只接受经过评审的合并。
- `test`：测试环境分支，用于测试部署。
- `dev-姓名缩写`：个人开发分支，例如 `dev-zs`。

如果项目使用其他分支名，需要同步修改：

- `.github/workflows/Backend.yml`
- `.github/workflows/Frontend.yml`
- 团队协作规范中的 PR 目标分支

### 3. 后端运行配置

后端必须配置：

- MySQL 地址、端口、库名、用户名、密码。
- Redis 地址、端口、DB、密码、key 前缀。
- Django `SECRET_KEY`。
- `ALLOWED_HOSTS`。
- `CSRF_TRUSTED_ORIGINS`。
- `CORS_ORIGIN_ALLOW_ALL` / `CORS_ALLOWED_ORIGINS`。
- JWT 有效期。
- Gunicorn worker、thread、timeout。

详细说明见 [Backend/README.md](Backend/README.md)。

### 4. 前端运行配置

前端必须配置：

- `VITE_APP_TITLE`：浏览器标题/应用标题。
- `VITE_API_BASE_URL`：浏览器请求后端的基础地址。
- `VITE_PROXY_API_TARGET`：本地开发时 Vite 代理到后端的地址。
- 首页、登录注册页、用户资料组件中的产品文案和业务入口。
- 路由路径和菜单结构。

详细说明见 [Frontend/README.md](Frontend/README.md)。

### 5. CI/CD 和服务器信息

GitHub Actions 默认按 `test` / `master` 部署测试和生产环境。需要在 GitHub Secrets 中配置：

- `ALI_DOCKER_USERNAME`
- `ALI_DOCKER_PASSWORD`
- `TEST_SSH_PRIVATE_KEY`
- `TEST_REMOTE_HOST`
- `TEST_REMOTE_USER`
- `TEST_DEPLOY_TARGET`
- `PROD_SSH_PRIVATE_KEY`
- `PROD_REMOTE_HOST`
- `PROD_REMOTE_USER`
- `PROD_DEPLOY_TARGET`

后端镜像推送到阿里云镜像仓库：

```text
registry.cn-hangzhou.aliyuncs.com/matrix-studio/<项目英文名>:test
registry.cn-hangzhou.aliyuncs.com/matrix-studio/<项目英文名>:prod
```

如果项目不使用阿里云镜像仓库，需要同步修改 `.github/workflows/Backend.yml` 和 `Backend/docker-compose-*.yml`。

## 本地启动

### 后端

```shell
cd Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

后端 `dev` 环境也使用 MySQL 和 Redis。启动前需要确保本机或远程 MySQL、Redis 可访问，并配置 `Backend/.env.dev`。

### 前端

```shell
cd Frontend
npm install
npm run dev
```

开发环境默认通过 `/api` 代理到 `http://127.0.0.1:8000`。

## 质量检查

后端：

```shell
cd Backend
make lint
make format-check
make test
python manage.py check --settings=Backend.settings.dev
python manage.py check --settings=Backend.settings.test
python manage.py check --settings=Backend.settings.prod
```

前端：

```shell
cd Frontend
npm run lint
npm run format:check
npm run type-check
npm run build
```

## 项目信息登记

新项目初始化后请补全以下信息，便于交接和运维。

### 服务器

- 测试环境服务器地址：
- 测试环境登录用户：
- 测试环境项目路径：
- 生产环境服务器地址：
- 生产环境登录用户：
- 生产环境项目路径：

### 域名

- 测试环境前端域名：
- 测试环境后端域名：
- 生产环境前端域名：
- 生产环境后端域名：

### 外部文档

- 需求文档：
- 原型/设计稿：
- 接口文档：
- 测试用例：
- 运维手册：

### 账号

- 测试环境普通账号：
- 测试环境管理员账号：
- 生产环境管理员账号：

不要把真实密码、密钥、数据库连接串写进 README 或代码仓库。真实敏感信息放在 GitHub Secrets、服务器环境变量或未提交的 `.env.*` 文件中。
