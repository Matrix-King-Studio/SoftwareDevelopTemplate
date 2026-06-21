import axios, { AxiosHeaders, type AxiosError, type AxiosInstance } from 'axios'
import { ApiError, ErrorType } from '@/types/error'
import type { ApiResponse } from '@/types/response'
import { HEADER_KEYS, BUSINESS_CODE } from '@/config/api'
import { cancelManager } from '@/utils/request-cancel'
import { tokenRefreshManager } from '@/utils/token-refresh'
import type { RequestConfig } from './request-config'

/** 将业务码规范化为数字 */
const normalizeBusinessCode = (code?: number | string): number | undefined => {
  if (typeof code === 'number') return code
  if (typeof code === 'string') {
    const n = Number(code)
    return Number.isNaN(n) ? undefined : n
  }
  return undefined
}

/** 判断是否应尝试刷新 Token */
const shouldRefreshToken = (
  config: RequestConfig | undefined,
  enableTokenRefresh: boolean,
  status?: number,
  code?: number | string
): boolean => {
  const normalizedCode = normalizeBusinessCode(code)
  return !!(
    config &&
    enableTokenRefresh &&
    !config.skipTokenRefresh &&
    !config._retryAfterRefresh &&
    (status === BUSINESS_CODE.UNAUTHORIZED || normalizedCode === BUSINESS_CODE.UNAUTHORIZED)
  )
}

/** 使用新 Token 重放原始请求 */
const retryRequestWithFreshToken = async (
  config: RequestConfig,
  axiosInstance: AxiosInstance
): Promise<unknown> => {
  const newToken = await tokenRefreshManager.handleRefresh(axiosInstance)
  const headers = new AxiosHeaders(config.headers as Record<string, string>)

  config._retryAfterRefresh = true
  config._skipDedupOnce = true
  headers.set(HEADER_KEYS.AUTHORIZATION, `Bearer ${newToken}`)
  config.headers = headers

  return axiosInstance.request(config)
}

interface HandleResolvedApiErrorParams {
  config?: RequestConfig
  axiosInstance: AxiosInstance
  enableTokenRefresh: boolean
  status?: number
  code?: number | string
  message?: string
  errorType: ErrorType
  originalError?: unknown
  responseData?: unknown
}

/** 统一处理已解析的 API 错误（401 刷新重试、403 跳转等） */
export const handleResolvedApiError = async ({
  config,
  axiosInstance,
  enableTokenRefresh,
  status,
  code,
  message,
  errorType,
  originalError,
  responseData,
}: HandleResolvedApiErrorParams): Promise<unknown> => {
  const normalizedCode = normalizeBusinessCode(code)

  // 401: 尝试刷新 Token 后重放请求
  if (shouldRefreshToken(config, enableTokenRefresh, status, normalizedCode)) {
    try {
      return await retryRequestWithFreshToken(config!, axiosInstance)
    } catch {
      tokenRefreshManager.redirectToLogin()
      throw new ApiError(
        ErrorType.HTTP_ERROR,
        '登录已过期，请重新登录',
        BUSINESS_CODE.UNAUTHORIZED,
        BUSINESS_CODE.UNAUTHORIZED
      )
    }
  }

  // 403: 无权限
  if (status === BUSINESS_CODE.FORBIDDEN || normalizedCode === BUSINESS_CODE.FORBIDDEN) {
    throw new ApiError(
      ErrorType.HTTP_ERROR,
      message || '没有权限访问该资源',
      BUSINESS_CODE.FORBIDDEN,
      BUSINESS_CODE.FORBIDDEN,
      originalError,
      responseData
    )
  }

  throw new ApiError(
    errorType,
    message || (status ? `请求失败 (${status})` : '请求失败'),
    status,
    normalizedCode,
    originalError,
    responseData
  )
}

/** 处理 axios 错误（网络错误、取消、HTTP 错误等） */
export const handleError = async (
  error: AxiosError<ApiResponse>,
  axiosInstance: AxiosInstance,
  enableTokenRefresh: boolean
): Promise<unknown> => {
  const config = error.config as RequestConfig

  // 清理已完成的请求登记
  if (config) {
    cancelManager.clearRequest(
      config.url || '',
      config.method || 'get',
      config.params || config.data
    )
  }

  // 请求取消
  if (axios.isCancel(error)) {
    throw new ApiError(ErrorType.CANCEL_ERROR, '请求已取消')
  }

  // 网络错误（无响应）
  if (!error.response) {
    throw new ApiError(
      ErrorType.NETWORK_ERROR,
      '网络连接失败，请检查网络设置',
      undefined,
      undefined,
      error
    )
  }

  const { response } = error
  const { status, data } = response
  const responseMessage = typeof data?.message === 'string' ? data.message : undefined

  return handleResolvedApiError({
    config,
    axiosInstance,
    enableTokenRefresh,
    status,
    code: data?.code,
    message: responseMessage || `请求失败 (${status})`,
    errorType: ErrorType.HTTP_ERROR,
    originalError: error,
    responseData: data?.data,
  })
}
