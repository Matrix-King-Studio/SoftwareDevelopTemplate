/**
 * 账户 API 模块。
 *
 * 认证方案为 JWT Bearer + 刷新令牌,接口字段与后端 Account 应用保持一致。
 *
 * ⚠️ 认证方案为 JWT Bearer + 刷新令牌，需后端配合：
 *   - 登录 `POST /auth/login/` 返回 data: { access_token, refresh_token, user }
 *   - 注册 `POST /auth/registration/` 返回注册结果
 *   - 当前用户 `GET /auth/user/` 返回 data: UserInfo
 *   - 登出 `POST /auth/logout/`
 *   - 刷新 `POST /auth/token/refresh/`（见 utils/token-refresh.ts）
 *
 * 若后端认证路径或字段发生变化,需要同步调整本模块与 `utils/token-refresh.ts`。
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
 * @returns 注册结果
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
