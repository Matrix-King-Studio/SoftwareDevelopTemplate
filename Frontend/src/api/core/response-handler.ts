import type { AxiosResponse } from 'axios'
import { ApiError, ErrorType } from '@/types/error'
import { cancelManager } from '@/utils/request-cancel'
import type { RequestConfig } from './request-config'

/**
 * 处理响应：校验业务码，成功则返回 response.data
 *
 * 约定后端返回 `{ code, message, data }`，code 在 [200, 300) 之间视为成功；
 * 否则抛出 BUSINESS_ERROR 类型的 ApiError。
 */
export const handleResponse = (response: AxiosResponse): unknown => {
  const config = response.config as RequestConfig

  cancelManager.clearRequest(config.url || '', config.method || 'get', config.params || config.data)

  const { data } = response

  // 校验业务状态码 data.code（2xx 为成功）
  if (data && typeof data === 'object' && 'code' in data) {
    const code = data.code as number
    const responseMessage =
      typeof (data as { message?: unknown }).message === 'string'
        ? (data as { message: string }).message
        : undefined

    if (code < 200 || code >= 300) {
      throw new ApiError(
        ErrorType.BUSINESS_ERROR,
        responseMessage || '业务错误',
        response.status,
        code,
        undefined,
        data.data
      )
    }
  }

  return data
}
