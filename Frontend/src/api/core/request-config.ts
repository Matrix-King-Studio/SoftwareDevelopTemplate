import type { AxiosRequestConfig } from 'axios'
import type { CacheConfig } from '@/utils/request-cache'

/** 去重策略：cancel-old 取消旧请求（默认），reject-new 拒绝新请求 */
export type DedupStrategy = 'cancel-old' | 'reject-new'

/**
 * 扩展的请求配置
 *
 * 在 AxiosRequestConfig 基础上增加项目请求层自定义的控制项。
 */
export interface RequestConfig extends AxiosRequestConfig {
  /** 是否跳过认证（登录/注册等匿名接口设为 true） */
  skipAuth?: boolean
  /** 是否跳过 Trace ID 注入 */
  skipTraceId?: boolean
  /** 是否启用请求去重（默认开启），可指定策略 */
  enableDedup?: boolean | DedupStrategy
  /** 是否跳过 Token 刷新等待 */
  skipTokenRefresh?: boolean
  /** 是否已在 refresh 后重试过（内部标记，勿手动设置） */
  _retryAfterRefresh?: boolean
  /** 是否跳过去重一次（内部标记，刷新重试时使用） */
  _skipDedupOnce?: boolean
  /** GET 请求缓存配置 */
  cache?: CacheConfig
}
