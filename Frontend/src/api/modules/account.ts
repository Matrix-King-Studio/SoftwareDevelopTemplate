/**
 * 账户 API 模块（示例）
 *
 * 这是“标准业务模块范式”示例：每个业务域一个文件，从 `@/api/instance` 导入
 * request 发起请求，统一以 `ApiResponse<T>` 标注返回类型。
 *
 * ⚠️ 认证方案为 JWT Bearer + 刷新令牌，需后端配合：
 *   - 登录 `POST /auth/login/` 返回 data: { access_token, refresh_token, user }
 *   - 注册 `POST /auth/registration/` 返回注册结果
 *   - 当前用户 `GET /auth/user/` 返回 data: UserInfo
 *   - 登出 `POST /auth/logout/`
 *   - 刷新 `POST /auth/token/refresh/`（见 utils/token-refresh.ts）
 *
 * 若后端仍为 Django dj-rest-auth 的 Token 方案（返回 data.key），
 * 需后端切换到 SimpleJWT 等 JWT 方案后，本模块才能直接联调。
 */

import { request } from '@/api/instance'
import type { ApiResponse } from '@/types/response'
import type { AuthTokens, LoginParams, RegisterParams, UserInfo } from '@/types/auth'

/**
 * 用户登录
 *
 * @param data - 登录参数（用户名 + 密码）
 * @returns 令牌与用户信息
 */
export function login(data: LoginParams) {
  return request.post<ApiResponse<AuthTokens>>('/auth/login/', data, {
    // 登录接口为匿名接口，无需注入旧 token
    skipAuth: true,
  })
}

/**
 * 用户注册
 *
 * @param data - 注册参数
 * @returns 注册结果（结构由后端决定，模板用 unknown 占位）
 */
export function register(data: RegisterParams) {
  return request.post<ApiResponse<unknown>>('/auth/registration/', data, {
    skipAuth: true,
  })
}

/**
 * 获取当前登录用户信息
 *
 * @returns 当前用户资料
 */
export function getCurrentUser() {
  return request.get<ApiResponse<UserInfo>>('/auth/user/')
}

/**
 * 用户登出
 *
 * @returns 登出结果
 */
export function logout() {
  return request.post<ApiResponse<null>>('/auth/logout/')
}
