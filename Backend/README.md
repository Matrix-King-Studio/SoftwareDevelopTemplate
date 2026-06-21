# {{ProjectChineseName}}-后端

本项目后端基于 Django 项目模板创建，提前内置了 DRF 等第三方开发库，可以极大的提高开发效率，避免重复造轮子。

跟标准的 Django 项目的区别还有：
1. settings 配置文件转移到了 Backend/Backend/settings 文件夹内，base.py 中是基础配置，dev.py 代表的是开发环境配置，test.py 代表的是测试环境配置，prod.py 代表的是生产环境配置；
2. startapp 创建的应用转移到了 Backend/Backend/apps 文件夹内，每一个文件夹代表了一个应用，如果要新建应用的话，需要先 `cd Backend/apps`然后在再`python ../../manage.py startapp ApplicationName`（注意应用首字母要大写）；
3. WSGI 入口按环境命名：`wsgi_dev.py` 是本地开发环境，`wsgi_test.py` 是测试环境，`wsgi_prod.py` 是生产环境；Gunicorn 自身配置放在 `gunicorn_config.py`。

## 快速开始

1. 项目代码拉取下来后，首先需要迁移数据库

```shell
python manage.py makemigrations
python manage.py migrate
```

2. 创建超级管理员账户

```shell
python manage.py createsuperuser
```

开发环境和测试环境，用户名和密码在都是 admin。

3. 在本地（一般是自己的电脑）开发的话，通过 `python manage.py runserver`启动，默认加载的是 `Backend/Backend/settings/dev.py`，即在本地创建一个 db.sqlite3 数据库，所有的开发数据都在本地；

## 自动部署

本地开发完成后，代码需要上传到 GitHub 自己的分支，然后创建 PR 合并到 test 分支，此时会触发测试环境的自动部署，模板中的默认配置可能会导致部署失败，因此需要修改一下 `docker-compose.yml` 文件和 `.github\workflows\Backend.yml` 中的占位符。

全局搜索关键词并替换：
- {{DOCKER_NAMESPACE}}：其替换为这个项目的英文名称，注意要小写；
- {{test_django_port}} / {{prod_django_port}}：将其替换为测试/生产环境的端口；
- {{test_mysql_*}} and {{test_redis_*}}：将其替换为测试/生产环境的配置信息。

## API 架构与规范

本模板内置一套企业级通用 API 基础设施,核心代码位于 `Backend/utils/`。

### 统一响应格式

所有接口(成功与失败)均返回固定结构:

```json
{ "code": 200, "message": "success", "data": {}, "requestId": "uuid" }
```

- `code`：业务/HTTP 状态码,2xx 表示成功;
- `message`：提示信息;
- `data`：业务数据,无数据时为 `{}`;
- `requestId`：本次请求唯一 ID,同时写入响应头 `X-Request-Id`,
  优先复用前端注入的 `X-Trace-Id`,用于前后端日志链路关联。

### 目录结构

```
Backend/
├── utils/
│   ├── drf/
│   │   ├── api.py                StandardAPIView 视图基类 + success/error_response
│   │   ├── pagination.py         StandardPageNumberPagination(count/page/page_size/results)
│   │   └── exception_handler.py  全局异常处理(校验错误→可读 message、DB/Redis→507、403→401、兜底 500)
│   ├── auth/
│   │   ├── token_service.py      JWT 签发/解析/轮换/失效(基于 token_version)
│   │   ├── authentication.py     BearerTokenAuthentication(Bearer JWT 认证后端)
│   │   └── permissions.py        IsActiveUser / IsAdminRole 等通用权限
│   └── log/
│       ├── request_id.py         requestId 线程本地存取
│       └── middleware.py         RequestLogMiddleware(生成/注入 requestId + 请求日志脱敏)
└── apps/Account/
    ├── models.py                 自定义 User(AbstractUser + role/status/token_version)
    ├── serializers/auth.py       Login/Register/RefreshToken/UserInfo 序列化器
    ├── views/auth.py             登录/注册/当前用户/登出/刷新视图
    └── urls.py                   auth/ 路由
```

### 认证方案(JWT Bearer + 刷新令牌)

- **access_token**：短效令牌(默认 30 分钟),请求头 `Authorization: Bearer <token>`;
- **refresh_token**：长效令牌(默认 7 天),用于续签 access;
- **token_version**：用户表字段,登出/改密时递增,使该用户历史令牌**全部失效**;
- JWT 有效期等参数在 `settings/base.py` 的 JWT 段配置,支持环境变量覆盖。

认证接口(与前端 `Frontend/src/api/modules/account.ts` 对齐):

| 接口 | 方法 | 说明 | 认证 |
| --- | --- | --- | --- |
| `/auth/registration/` | POST | 注册(username/email/password1/password2) | 公开 |
| `/auth/login/` | POST | 登录(username/password) | 公开,限流 10/min |
| `/auth/user/` | GET | 获取当前用户 | 需 access |
| `/auth/logout/` | POST | 登出(递增 token_version) | 需 access |
| `/auth/token/refresh/` | POST | 刷新(body: refresh_token) | 公开 |

> 前端经 Vite 代理(`/api` → 后端,rewrite 去掉 `/api`),故前端 `/api/auth/login/`
> 实际命中后端 `/auth/login/`。

### 编写新业务接口

视图继承 `StandardAPIView`,用 `self.success()` / `self.error()` / `self.paginate()`:

```python
from rest_framework.permissions import IsAuthenticated
from Backend.utils.drf.api import StandardAPIView

class ArticleListView(StandardAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Article.objects.all()
        return self.paginate(request, qs, ArticleSerializer)
```

### Redis 与缓存

- `dev` 环境使用进程内存缓存(LocMemCache),**不依赖 Redis,开箱即跑**;
- `test` / `prod` 使用 `django-redis` 接入 Redis,连接信息从环境变量读取
  (`REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` / `REDIS_PASSWORD`)。

### 依赖

新增:`PyJWT`、`redis`、`django-redis`。
已移除旧的 Token 认证方案(`dj-rest-auth` / `allauth` / `rest_framework.authtoken`),
改为纯自定义 JWT。

## 注意事项

1. 本地开发数据库迁移的时候，一定要在本地执行完 `python manage.py makemigrations` 和 `python manage.py migrate` 之后，将生成的 migrations 文件进行 `git add`，然后再提交代码。这是因为 Github Actions 自动部署服务器的时候也会执行这两条命令，如果本地没有 migrations 文件而服务器上生成了的话，后续可能会导致代码仓库中的 migrations 文件跟服务器上的 migrations 文件不一致；

2. 本模板使用自定义用户模型 `AUTH_USER_MODEL = "Account.User"`,该设置必须在项目**首次 migrate 之前**确定。模板已在零迁移状态下落地,初始迁移文件 `Account/migrations/0001_initial.py` 已生成,直接使用即可;后续若需调整 User 字段,按常规迁移流程执行。
