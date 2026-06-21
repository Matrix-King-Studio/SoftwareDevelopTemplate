import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'
import { generateRequestKey } from '@/utils/request-helpers'
import { cacheManager } from '@/utils/request-cache'
import { getToken } from '@/utils/token'
import { setupInterceptors } from './request-interceptors'
import type { RequestConfig } from './request-config'

type CacheScope = NonNullable<RequestConfig['cache']>['scope']

interface TokenCachePayload {
  /** JWT 所属终端，用于区分 user/admin 等登录端 */
  terminal?: unknown
  /** JWT 主体 ID，用于区分同浏览器切换账号 */
  subject_id?: unknown
  /** JWT 版本号，用于密码重置或登出后隔离旧缓存 */
  token_version?: unknown
}

/** 解码 JWT payload 的 base64url 字段 */
const decodeBase64Url = (value: string): string => {
  const base64 = value.replace(/-/g, '+').replace(/_/g, '/')
  const normalizedBase64 = base64.padEnd(Math.ceil(base64.length / 4) * 4, '=')

  return window.atob(normalizedBase64)
}

/** 解析 JWT payload，失败时返回 null */
const parseTokenPayload = (token: string): TokenCachePayload | null => {
  const [, payload] = token.split('.')

  if (!payload) return null

  try {
    const parsed = JSON.parse(decodeBase64Url(payload)) as unknown

    if (!parsed || typeof parsed !== 'object') return null

    return parsed as TokenCachePayload
  } catch {
    return null
  }
}

/** 为无法解析的 token 生成短哈希，避免把完整 token 放入缓存 key */
const hashToken = (token: string): string => {
  let hash = 0

  for (let index = 0; index < token.length; index += 1) {
    hash = (hash * 31 + token.charCodeAt(index)) >>> 0
  }

  return hash.toString(36)
}

/** 获取 auth 缓存命名空间，优先使用后端 token 主体信息 */
const getAuthCacheNamespace = (): string => {
  const token = getToken()

  if (!token) return 'auth:anonymous'

  const payload = parseTokenPayload(token)

  if (
    payload?.terminal !== undefined &&
    payload.subject_id !== undefined &&
    payload.token_version !== undefined
  ) {
    return `auth:${String(payload.terminal)}:${String(payload.subject_id)}:${String(
      payload.token_version
    )}`
  }

  return `auth:${hashToken(token)}`
}

/** 根据请求配置生成带 public/auth 隔离的 GET 缓存 key */
const generateScopedCacheKey = (url: string, config: RequestConfig): string => {
  const scope: CacheScope = config.cache?.scope || (config.skipAuth ? 'public' : 'auth')
  const namespace = scope === 'public' ? 'public' : getAuthCacheNamespace()

  return `${namespace}:${generateRequestKey(url, 'GET', config.params)}`
}

/**
 * 请求客户端
 *
 * 对 axios 实例做语义化封装，统一返回 `response.data`（已被响应拦截器处理为业务体）。
 * 泛型 T 即业务返回类型，通常为 `ApiResponse<XXX>`。
 *
 * GET 请求支持缓存：在 config.cache.enable=true 时启用，并对并发的相同请求做合并。
 */
export class Request {
  private instance: AxiosInstance
  private enableTokenRefresh: boolean

  /** 暴露底层 axios 实例，供外部模块按需挂载拦截器 */
  get axiosInstance(): AxiosInstance {
    return this.instance
  }

  constructor(config: AxiosRequestConfig, enableTokenRefresh = true) {
    this.instance = axios.create(config)
    this.enableTokenRefresh = enableTokenRefresh
    setupInterceptors(this.instance, this.enableTokenRefresh)
  }

  async get<T = unknown>(url: string, config?: RequestConfig): Promise<T> {
    if (config?.cache?.enable) {
      const cacheKey = generateScopedCacheKey(url, config)
      if (cacheManager.has(cacheKey)) {
        return cacheManager.get<T>(cacheKey) as T
      }

      const pendingRequest = cacheManager.getPending<T>(cacheKey)
      if (pendingRequest) return pendingRequest

      const request = this.instance.get(url, config).then(result => {
        cacheManager.set(cacheKey, result as T, config.cache?.ttl)
        return result as T
      })

      return cacheManager.setPending(cacheKey, request)
    }
    return this.instance.get(url, config) as Promise<T>
  }

  post<T = unknown>(url: string, data?: unknown, config?: RequestConfig): Promise<T> {
    return this.instance.post(url, data, config) as Promise<T>
  }

  put<T = unknown>(url: string, data?: unknown, config?: RequestConfig): Promise<T> {
    return this.instance.put(url, data, config) as Promise<T>
  }

  patch<T = unknown>(url: string, data?: unknown, config?: RequestConfig): Promise<T> {
    return this.instance.patch(url, data, config) as Promise<T>
  }

  delete<T = unknown>(url: string, config?: RequestConfig): Promise<T> {
    return this.instance.delete(url, config) as Promise<T>
  }

  request<T = unknown>(config: RequestConfig): Promise<T> {
    return this.instance.request(config) as Promise<T>
  }
}
