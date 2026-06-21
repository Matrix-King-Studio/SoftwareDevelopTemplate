import type { AxiosRequestConfig } from 'axios'

/**
 * 后端 API 请求基础配置
 *
 * baseURL 从环境变量读取：
 * - 开发环境：/api（由 Vite proxy 转发到本地后端）
 * - 生产/测试：绝对域名 或 /api（由 Nginx 反代）
 */
export const API_CONFIG: AxiosRequestConfig = {
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
}

/** 本地存储键名（token 持久化） */
export const STORAGE_KEYS = {
  /** 访问令牌（access token） */
  AUTH_TOKEN: 'auth_token',
  /** 刷新令牌（refresh token） */
  REFRESH_TOKEN: 'refresh_token',
} as const

/** 请求头键名 */
export const HEADER_KEYS = {
  /** 认证头，注入 `Bearer <access_token>` */
  AUTHORIZATION: 'Authorization',
  /** 链路追踪 ID，便于前后端日志关联排查 */
  TRACE_ID: 'X-Trace-Id',
} as const

/**
 * 业务/HTTP 状态码
 *
 * 约定：后端统一响应体 `{ code, message, data }` 中的 code 与 HTTP status 含义对齐。
 */
export const BUSINESS_CODE = {
  SUCCESS: 200,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  TOO_MANY_REQUESTS: 429,
  INTERNAL_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
} as const

/** 环境相关开关 */
export const ENV_CONFIG = {
  api: {
    /** 是否启用请求去重（避免短时间内重复请求） */
    enableDedup: true,
    /** 是否启用请求日志（仅开发环境，自动脱敏敏感字段） */
    enableRequestLog: import.meta.env.DEV,
  },
} as const
