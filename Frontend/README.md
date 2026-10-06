# {{ProjectChineseName}} 前端

前端基于 Vue 3 + TypeScript + Vite，内置 Element Plus、Pinia、Vue Router、Axios 请求层、Token 自动刷新、请求去重、GET 缓存、Trace ID 和基础账号页面。

拿到这份前端后，需要先改项目名称、环境变量、接口地址、首页文案、路由结构和部署配置，再继续业务开发。

## 技术栈

- Vue 3 + `<script setup>` + TypeScript
- Vite 7
- Pinia
- Vue Router
- Element Plus
- Tailwind CSS
- Axios
- ESLint + Prettier
- Vitest
- Playwright

## 拿到模板后必须修改

### 0. 全局搜索替换

前端保留 `{{...}}` 占位符用于快速初始化。先按根目录 [README.md](../README.md) 的全局替换表处理以下关键 token：

- `{{ProjectChineseName}}`
- `{{FRONTEND_PACKAGE_NAME}}`
- `{{TEST_FRONTEND_API_BASE_URL}}`
- `{{PROD_FRONTEND_API_BASE_URL}}`

### 1. 项目名称

需要修改：

- `Frontend/package.json` 的 `name`。
- `Frontend/.env.development` 的 `VITE_APP_TITLE`。
- `Frontend/.env.test` 的 `VITE_APP_TITLE`。
- `Frontend/.env.prod` 的 `VITE_APP_TITLE`。
- `Frontend/src/views/Index.vue` 首页文案。
- `Frontend/index.html` 中的标题（如果后续添加或已有静态 title）。

命名建议：

```text
package name: smart-campus-frontend
VITE_APP_TITLE=智慧校园
```

### 2. API 地址

环境文件：

| 文件               | 用途     | 关键变量                                     |
| ------------------ | -------- | -------------------------------------------- |
| `.env.development` | 本地开发 | `VITE_API_BASE_URL`、`VITE_PROXY_API_TARGET` |
| `.env.test`        | 测试构建 | `VITE_API_BASE_URL`                          |
| `.env.prod`        | 生产构建 | `VITE_API_BASE_URL`                          |

开发环境通常保持：

```env
VITE_API_BASE_URL=/api
VITE_PROXY_API_TARGET=http://127.0.0.1:8000
```

这样浏览器请求 `/api/auth/login/`，Vite dev server 会代理到 `http://127.0.0.1:8000/auth/login/`。

测试/生产环境有两种方式：

```env
# 方式一：前端直接请求后端域名
VITE_API_BASE_URL=https://api.example.com

# 方式二：保持 /api，由 Nginx 反向代理到后端
VITE_API_BASE_URL=/api
```

选方式二时，服务器必须配置 `/api` 反向代理，并去掉 `/api` 前缀或与后端路由保持一致。

### 3. 后端接口契约

当前前端账号模块要求后端提供：

| 前端请求                        | 后端实际接口                | 说明       |
| ------------------------------- | --------------------------- | ---------- |
| `POST /api/auth/login/`         | `POST /auth/login/`         | 登录       |
| `POST /api/auth/registration/`  | `POST /auth/registration/`  | 注册       |
| `GET /api/auth/user/`           | `GET /auth/user/`           | 当前用户   |
| `POST /api/auth/logout/`        | `POST /auth/logout/`        | 登出       |
| `POST /api/auth/token/refresh/` | `POST /auth/token/refresh/` | 刷新 token |

统一响应结构：

```ts
interface ApiResponse<T> {
  code: number
  message: string
  data: T
  requestId?: string
}
```

登录/注册返回：

```ts
{
  access_token: string
  refresh_token: string
  expires_in: number
  user: UserInfo
}
```

如果后端路径、字段名或认证方案变化，需要同步修改：

- `src/api/modules/account.ts`
- `src/types/auth.ts`
- `src/utils/token-refresh.ts`
- `src/config/api.ts`

### 4. 页面和路由

默认路由：

- `/`：首页
- `/signup_login`：登录注册页

新项目通常需要修改：

- `src/router/index.ts`：业务路由。
- `src/views/Index.vue`：首页或工作台首页。
- `src/views/account/SignupLogin.vue`：登录注册页布局和文案。
- `src/components/account/*`：账号相关组件。
- `src/styles/*`：主题变量、全局样式。

如果登录页路径变化，必须同步修改 `src/utils/token-refresh.ts` 中登录过期后的跳转路径。

### 5. 权限和用户信息

当前用户类型在 `src/types/auth.ts`：

```ts
interface UserInfo {
  id: number
  username: string
  email?: string
  role?: string
  status?: string
  avatar?: string
  date_joined?: string
}
```

如果后端增加组织、部门、菜单权限、按钮权限等字段，需要同步更新：

- `src/types/auth.ts`
- `src/stores/account.ts`
- 用户资料组件
- 路由守卫或权限判断逻辑

### 6. CI/CD

前端部署工作流：`.github/workflows/Frontend.yml`

默认行为：

- 推送到 `test`：执行 `npm run build -- --mode test`
- 推送到 `master`：执行 `npm run build -- --mode prod`
- 上传 `Frontend/dist/*` 到远程服务器

需要确认：

- 分支名是否符合项目规范。
- `TEST_DEPLOY_TARGET` / `PROD_DEPLOY_TARGET` 是否是前端静态文件目录。
- 服务器 Nginx 是否指向前端构建目录。
- `/api` 是否正确反向代理到后端。

## 本地开发

```shell
cd Frontend
npm install
npm run dev
```

默认开发服务由 Vite 启动。后端默认代理目标在 `.env.development` 中配置。

## 可用脚本

| 脚本                   | 说明                       |
| ---------------------- | -------------------------- |
| `npm run dev`          | 启动开发服务器             |
| `npm run build`        | 类型检查 + 默认构建        |
| `npm run build:dev`    | 使用 development mode 构建 |
| `npm run build:test`   | 使用 test mode 构建        |
| `npm run build:prod`   | 使用 prod mode 构建        |
| `npm run type-check`   | TypeScript 类型检查        |
| `npm run lint`         | ESLint 检查                |
| `npm run lint:fix`     | ESLint 自动修复            |
| `npm run format`       | Prettier 格式化            |
| `npm run format:check` | Prettier 格式检查          |
| `npm run test:unit`    | Vitest 单元测试            |
| `npm run test:e2e`     | Playwright E2E 测试        |

## API 请求层

目录：

```text
src/
├── api/
│   ├── core/                  Request 类、拦截器、错误处理
│   ├── instance.ts            全局 request 实例
│   ├── modules/account.ts     账号接口
│   └── index.ts               API 出口
├── config/api.ts              API 基础配置
├── types/                     响应、错误、认证类型
└── utils/                     token、刷新、缓存、取消、消息提示
```

内置能力：

- 统一响应解析。
- 统一错误包装为 `ApiError`。
- 401 自动刷新 access token。
- 并发 401 只刷新一次。
- 请求去重。
- GET 内存缓存。
- `X-Trace-Id` 注入。
- 开发环境请求日志脱敏。

新增业务模块时，在 `src/api/modules/` 下按业务域建文件，并从 `@/api/instance` 导入 `request`。

## 测试

安装 Playwright 浏览器内核：

```shell
npx playwright install
```

执行：

```shell
npm run test:unit
npm run test:e2e
```

## 上线前检查清单

- `VITE_APP_TITLE` 已替换为真实项目名。
- `VITE_API_BASE_URL` 指向正确后端。
- Nginx `/api` 代理规则与后端路由一致。
- 登录过期跳转路径正确。
- 首页、登录页和用户资料文案已替换。
- `npm run lint` 通过。
- `npm run format:check` 通过。
- `npm run type-check` 通过。
- `npm run build:prod` 通过。
