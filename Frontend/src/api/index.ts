/**
 * API 层统一出口
 *
 * 使用方式：
 *   import { request, accountApi } from '@/api'
 *   import type { ApiResponse } from '@/types/response'
 *
 * 业务模块按域拆分在 `./modules/` 下，并在此处聚合导出。
 */

// 请求实例与核心类型
export { request } from './instance'
export { Request } from './core'
export type { RequestConfig, DedupStrategy } from './core'

// 业务模块（按需扩展）
export * as accountApi from './modules/account'
