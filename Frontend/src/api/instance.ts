import { Request } from '@/api/core'
import { API_CONFIG } from '@/config/api'

/**
 * 后端 API 请求实例（全局单例）
 *
 * 业务模块统一从这里导入 request 发起请求，例如：
 *   import { request } from '@/api/instance'
 *   const res = await request.get<ApiResponse<User>>('/user/profile/')
 */
export const request = new Request(API_CONFIG, true)
