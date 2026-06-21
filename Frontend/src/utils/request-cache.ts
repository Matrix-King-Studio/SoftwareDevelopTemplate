interface CacheItem<T> {
  data: T
  expireTime: number
}

/** GET 请求缓存配置 */
export interface CacheConfig {
  /** 是否启用缓存 */
  enable?: boolean
  /** 缓存隔离范围：public 跨登录态复用，auth 按当前 token 主体隔离 */
  scope?: 'public' | 'auth'
  /** 缓存时间（毫秒），默认 5000ms */
  ttl?: number
}

/**
 * 内存缓存管理器
 *
 * 用于缓存 GET 请求结果，并对“正在进行中的相同请求”做合并（pendingRequests），
 * 避免并发重复请求打到后端。
 */
class CacheManager {
  private cache = new Map<string, CacheItem<unknown>>()
  private pendingRequests = new Map<string, Promise<unknown>>()

  /** 写入缓存，ttl 毫秒后过期 */
  set<T>(key: string, data: T, ttl = 5000): void {
    this.cache.set(key, { data, expireTime: Date.now() + ttl })
  }

  /** 读取缓存，过期返回 null 并清除 */
  get<T>(key: string): T | null {
    const item = this.cache.get(key) as CacheItem<T> | undefined
    if (!item) return null
    if (Date.now() > item.expireTime) {
      this.cache.delete(key)
      return null
    }
    return item.data
  }

  /** 判断缓存是否存在且未过期 */
  has(key: string): boolean {
    const item = this.cache.get(key)
    if (!item) return false
    if (Date.now() > item.expireTime) {
      this.cache.delete(key)
      return false
    }
    return true
  }

  /** 删除指定缓存 */
  delete(key: string): void {
    this.cache.delete(key)
    this.pendingRequests.delete(key)
  }

  /** 清空全部缓存（登出时调用） */
  clear(): void {
    this.cache.clear()
    this.pendingRequests.clear()
  }

  /** 清理已过期缓存 */
  clearExpired(): void {
    const now = Date.now()
    this.cache.forEach((item, key) => {
      if (now > item.expireTime) {
        this.cache.delete(key)
      }
    })
  }

  /** 当前缓存条目数 */
  size(): number {
    return this.cache.size
  }

  /** 获取正在进行中的相同请求（用于请求合并） */
  getPending<T>(key: string): Promise<T> | null {
    return (this.pendingRequests.get(key) as Promise<T> | undefined) || null
  }

  /** 登记一个进行中的请求，完成后自动清除登记 */
  setPending<T>(key: string, request: Promise<T>): Promise<T> {
    this.pendingRequests.set(key, request)
    request
      .finally(() => {
        if (this.pendingRequests.get(key) === request) {
          this.pendingRequests.delete(key)
        }
      })
      .catch(() => undefined)
    return request
  }
}

export const cacheManager = new CacheManager()

let cleanupTimer: ReturnType<typeof setInterval> | null = null

/** 启动缓存清理定时器（仅初始化一次，建议在 main.ts 调用） */
export const ensureCacheCleanupStarted = (): void => {
  if (cleanupTimer !== null) return
  cleanupTimer = setInterval(() => {
    cacheManager.clearExpired()
  }, 60000)
}

/** 停止缓存清理定时器 */
export const stopCacheCleanup = (): void => {
  if (cleanupTimer !== null) {
    clearInterval(cleanupTimer)
    cleanupTimer = null
  }
}
