# [项目名称]-前端

本项目基于 Vue 3 + TypeScript + Vite 模板创建，内置 Element Plus、Pinia、Vue Router、
Tailwind CSS 等常用库，并封装了一套通用的 API 请求层与工程化规范（ESLint + Prettier），
可极大提高开发效率，避免重复造轮子。

## 技术栈

- **框架**：Vue 3（`<script setup>`）+ TypeScript
- **构建**：Vite 7
- **状态管理**：Pinia
- **路由**：Vue Router
- **UI**：Element Plus + Tailwind CSS
- **HTTP**：Axios（封装见 `src/api`）
- **代码规范**：ESLint（flat config）+ Prettier + EditorConfig

## 快速开始

```shell
npm install
npm run dev
```

## 可用脚本

| 脚本                   | 说明                                |
| ---------------------- | ----------------------------------- |
| `npm run dev`          | 启动开发服务器                      |
| `npm run build`        | 默认构建（type-check + vite build） |
| `npm run build:dev`    | 以 development 模式构建             |
| `npm run build:test`   | 以 test 模式构建（读 `.env.test`）  |
| `npm run build:prod`   | 以 prod 模式构建（读 `.env.prod`）  |
| `npm run type-check`   | 仅做 TypeScript 类型检查            |
| `npm run lint`         | ESLint 检查                         |
| `npm run lint:fix`     | ESLint 检查并自动修复               |
| `npm run format`       | Prettier 格式化全部源码             |
| `npm run format:check` | Prettier 仅检查格式是否一致         |
| `npm run test:unit`    | Vitest 单元测试                     |
| `npm run test:e2e`     | Playwright E2E 测试                 |

## 环境变量

环境文件位于项目根目录，按构建 `--mode` 自动加载：

| 文件               | 加载时机                             | 关键变量                                          |
| ------------------ | ------------------------------------ | ------------------------------------------------- |
| `.env.development` | `npm run dev` / `--mode development` | `VITE_API_BASE_URL=/api`、`VITE_PROXY_API_TARGET` |
| `.env.test`        | `--mode test`                        | `VITE_API_BASE_URL`（测试环境后端地址）           |
| `.env.prod`        | `--mode prod`                        | `VITE_API_BASE_URL`（生产环境后端地址）           |

- `VITE_API_BASE_URL`：API 基础地址。开发环境用 `/api`（经 Vite proxy 转发）；
  生产/测试可填后端绝对域名，或保持 `/api` 由 Nginx 反代。
- `VITE_PROXY_API_TARGET`：仅 dev server 使用的本地后端代理目标。

类型声明见 `src/env.d.ts`，新增 `VITE_` 变量时请同步补充。

## API 请求层

目录结构：

```
src/
├── config/api.ts            # API 基础配置、存储键、状态码、环境开关
├── types/
│   ├── response.ts          # ApiResponse / 分页类型
│   ├── error.ts             # ApiError 统一错误类
│   └── auth.ts              # 认证相关类型
├── utils/
│   ├── token.ts             # access/refresh token 存取
│   ├── token-refresh.ts     # 并发安全的 token 自动刷新
│   ├── request-cancel.ts    # 请求去重 / 取消
│   ├── request-cache.ts     # GET 内存缓存
│   ├── request-helpers.ts   # 请求 key / trace id 生成
│   └── message.ts           # Element Plus 统一消息提示
└── api/
    ├── core/                # Request 类 + 拦截器 + 错误/响应处理
    ├── instance.ts          # request 全局单例
    ├── modules/account.ts   # 业务模块示例
    └── index.ts             # 统一出口
```

### 基本用法

```ts
import { request } from '@/api/instance'
import type { ApiResponse } from '@/types/response'

// GET（带 5s 缓存）
const res = await request.get<ApiResponse<User>>('/user/profile/', {
  cache: { enable: true, ttl: 5000 },
})

// POST
await request.post<ApiResponse<null>>('/user/update/', { nickname: 'xxx' })
```

### 新增业务模块

在 `src/api/modules/` 下新建文件，参照 `account.ts` 范式：

```ts
import { request } from '@/api/instance'
import type { ApiResponse } from '@/types/response'

export function getList(params?: { page?: number }) {
  return request.get<ApiResponse<Item[]>>('/items/', { params })
}
```

### 内置能力

- **统一错误处理**：所有错误包装为 `ApiError`，可用 `isAuthError()` / `isBusinessError()` 等判断。
- **Token 自动刷新**：401 时自动用 refresh token 换取新 token 并重放请求，并发请求只刷新一次。
- **请求去重**：相同请求默认 `cancel-old`，可按需 `reject-new`（防表单重复提交）或关闭。
- **GET 缓存**：按 public/auth 维度隔离，避免切换账号串数据。
- **Trace ID**：自动注入 `X-Trace-Id`，便于前后端日志关联。
- **日志脱敏**：开发环境打印请求日志，password 等敏感字段自动打码。

### ⚠️ 后端契约（重要）

API 层采用 **JWT Bearer + 刷新令牌** 方案，且约定后端统一响应体 `{ code, message, data }`。
要让登录与自动刷新生效，后端需提供：

- 登录 `POST /api/auth/login/` → `data: { access_token, refresh_token, user }`
- 当前用户 `GET /api/auth/user/` → `data: UserInfo`
- 刷新 `POST /api/auth/token/refresh/`，body `{ refresh_token }` → `data: { access_token }`
- 业务错误用 `code`（2xx 成功），未认证返回 HTTP 401

若后端仍为 Django `dj-rest-auth` 的 Token 方案（登录返回 `data.key`），
请切换到 SimpleJWT 等 JWT 方案，或相应调整 `utils/token-refresh.ts` 与 `api/modules/account.ts`。

## 自动化测试

前端开发完成之后需要进行充分的测试。本模板采用
[Playwright](https://www.npmjs.com/package/playwright) 进行 E2E 自动化测试。

执行完 `npm install` 后，Playwright 已安装，但还需手动安装浏览器内核：

```shell
npx playwright install
```
