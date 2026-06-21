/** 错误类型常量 */
export const ErrorType = {
  /** 网络连接失败（无响应） */
  NETWORK_ERROR: 'NETWORK_ERROR',
  /** HTTP 错误（4xx/5xx） */
  HTTP_ERROR: 'HTTP_ERROR',
  /** 业务错误（HTTP 200 但 data.code 非 2xx） */
  BUSINESS_ERROR: 'BUSINESS_ERROR',
  /** 请求超时 */
  TIMEOUT_ERROR: 'TIMEOUT_ERROR',
  /** 请求被取消（去重 / 路由切换） */
  CANCEL_ERROR: 'CANCEL_ERROR',
  /** 未知错误 */
  UNKNOWN_ERROR: 'UNKNOWN_ERROR',
} as const

export type ErrorType = (typeof ErrorType)[keyof typeof ErrorType]

/**
 * 统一错误类
 *
 * 所有经由 API 层抛出的错误都会被包装成 ApiError，
 * 业务层可通过 `instanceof ApiError` 与其上的类型判断方法精确处理。
 */
export class ApiError extends Error {
  /** 错误类型 */
  type: ErrorType
  /** HTTP 状态码 */
  status?: number
  /** 业务状态码 */
  code?: number | string
  /** 原始错误对象（如 AxiosError） */
  originalError?: unknown
  /** 错误附带的业务数据 */
  data?: unknown

  constructor(
    type: ErrorType,
    message: string,
    status?: number,
    code?: number | string,
    originalError?: unknown,
    data?: unknown
  ) {
    super(message)
    this.name = 'ApiError'
    this.type = type
    this.status = status
    this.code = code
    this.originalError = originalError
    this.data = data
  }

  /** 是否为网络错误 */
  isNetworkError(): boolean {
    return this.type === ErrorType.NETWORK_ERROR
  }

  /** 是否为业务错误 */
  isBusinessError(): boolean {
    return this.type === ErrorType.BUSINESS_ERROR
  }

  /** 是否为未认证错误（401） */
  isAuthError(): boolean {
    return this.status === 401
  }

  /** 是否为无权限错误（403） */
  isForbiddenError(): boolean {
    return this.status === 403
  }
}
