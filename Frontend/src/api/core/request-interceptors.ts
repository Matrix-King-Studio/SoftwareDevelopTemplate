import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosHeaders } from 'axios'
import { ApiError } from '@/types/error'
import { HEADER_KEYS, ENV_CONFIG } from '@/config/api'
import { generateTraceId } from '@/utils/request-helpers'
import { cancelManager } from '@/utils/request-cancel'
import { getToken } from '@/utils/token'
import { tokenRefreshManager } from '@/utils/token-refresh'
import { handleResponse } from './response-handler'
import { handleError, handleResolvedApiError } from './error-handler'
import type { RequestConfig, DedupStrategy } from './request-config'

/** 解析去重策略 */
const resolveDedupStrategy = (enableDedup?: boolean | DedupStrategy): DedupStrategy | false => {
  if (enableDedup === false) return false
  if (enableDedup === true || enableDedup === undefined) return 'cancel-old'
  return enableDedup
}

/** 敏感字段列表，日志输出时脱敏 */
const SENSITIVE_KEYS = [
  'password',
  'password1',
  'password2',
  'code',
  'sms_code',
  'token',
  'refresh_token',
  'old_password',
  'new_password',
]

/** 对请求数据中的敏感字段进行脱敏处理 */
const sanitizeData = (data: unknown): unknown => {
  if (!data || typeof data !== 'object') return data
  const sanitized = { ...(data as Record<string, unknown>) }
  for (const key of SENSITIVE_KEYS) {
    if (key in sanitized) sanitized[key] = '***'
  }
  return sanitized
}

/** 请求拦截器 */
const requestInterceptor = async (
  config: InternalAxiosRequestConfig
): Promise<InternalAxiosRequestConfig> => {
  const customConfig = config as RequestConfig

  // 等待正在进行的 Token 刷新（避免携带旧 token 发出请求）
  if (!customConfig.skipTokenRefresh) {
    await tokenRefreshManager.waitForRefreshIfNeeded()
  }

  if (!config.headers) {
    config.headers = {} as AxiosHeaders
  }

  // 注入 Trace ID
  if (!customConfig.skipTraceId) {
    config.headers[HEADER_KEYS.TRACE_ID] = generateTraceId()
  }

  // 注入 Token（Bearer 方案）
  if (!customConfig.skipAuth) {
    const token = getToken()
    if (token) {
      config.headers[HEADER_KEYS.AUTHORIZATION] = `Bearer ${token}`
    }
  }

  // 请求去重
  if (customConfig._skipDedupOnce) {
    delete customConfig._skipDedupOnce
  } else if (ENV_CONFIG.api.enableDedup) {
    const strategy = resolveDedupStrategy(customConfig.enableDedup)
    if (strategy) {
      const controller = cancelManager.addPendingRequest(
        config.url || '',
        config.method || 'get',
        config.params || config.data,
        strategy
      )
      config.signal = controller.signal
    }
  }

  // 开发环境请求日志（敏感字段已脱敏）
  if (ENV_CONFIG.api.enableRequestLog) {
    console.warn('[API Request]', {
      method: config.method?.toUpperCase(),
      url: config.url,
      params: config.params,
      data: sanitizeData(config.data),
    })
  }

  return config
}

/** 响应成功拦截器 */
const responseFulfilledInterceptor = async (
  response: AxiosResponse,
  instance: AxiosInstance,
  enableTokenRefresh: boolean
): Promise<AxiosResponse> => {
  try {
    return handleResponse(response) as AxiosResponse
  } catch (error) {
    // 业务码非 2xx 时，handleResponse 抛 ApiError，这里交给统一错误处理（如 401 刷新）
    if (error instanceof ApiError) {
      return (await handleResolvedApiError({
        config: response.config as RequestConfig,
        axiosInstance: instance,
        enableTokenRefresh,
        status: error.status,
        code: error.code,
        message: error.message,
        errorType: error.type,
        originalError: error.originalError,
        responseData: error.data,
      })) as AxiosResponse
    }
    throw error
  }
}

/** 为指定 axios 实例安装请求/响应拦截器 */
export const setupInterceptors = (instance: AxiosInstance, enableTokenRefresh: boolean): void => {
  instance.interceptors.request.use(requestInterceptor, error => Promise.reject(error))

  instance.interceptors.response.use(
    response => responseFulfilledInterceptor(response, instance, enableTokenRefresh),
    error => handleError(error, instance, enableTokenRefresh)
  )
}
