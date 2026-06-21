/**
 * 标准 API 响应格式
 *
 * 后端约定统一返回 `{ code, message, data }`：
 * - code：业务状态码（2xx 表示成功）
 * - message：提示文案
 * - data：业务数据载荷
 */
export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

/** 分页查询参数 */
export interface PaginationParams {
  page: number
  pageSize: number
}

/** 分页响应数据（字段命名贴合 Django REST Framework 默认分页） */
export interface PaginationResponse<T> {
  /** 总条数 */
  count: number
  /** 当前页数据列表 */
  results: T[]
  /** 当前页码 */
  page: number
  /** 每页数量 */
  page_size: number
}
