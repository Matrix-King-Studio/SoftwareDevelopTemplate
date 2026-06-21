import axios, { type AxiosInstance } from 'axios'
import { API_CONFIG } from '@/config/api'
import { setToken, getRefreshToken, clearAllTokens } from '@/utils/token'
import type { ApiResponse } from '@/types/response'
import type { RefreshTokenResult } from '@/types/auth'
import router from '@/router'

interface RefreshQueueItem {
  resolve: (token: string) => void
  reject: (error: unknown) => void
}

/**
 * Token 刷新管理器
 *
 * 负责在 access_token 过期（401）时，用 refresh_token 换取新的 access_token，
 * 并保证“并发多个 401 请求只触发一次刷新”，其余请求排队等待刷新结果。
 *
 * ⚠️ 后端契约：需提供刷新端点 `POST {baseURL}/auth/token/refresh/`，
 *    请求体 `{ refresh_token }`，成功返回 `{ code, message, data: { access_token } }`。
 *    若后端端点路径或字段不同，请同步修改 refreshToken() 内的实现。
 */
class TokenRefreshManager {
  private isRefreshing = false
  private refreshQueue: RefreshQueueItem[] = []

  /** 使用 refresh_token 换取新的 access_token */
  private async refreshToken(_axiosInstance: AxiosInstance): Promise<string> {
    const refreshToken = getRefreshToken()
    if (!refreshToken) {
      throw new Error('未找到 refresh token')
    }

    // 使用独立的 axios 调用，避免走主实例拦截器造成递归刷新
    const response = await axios.post<ApiResponse<RefreshTokenResult>>(
      `${API_CONFIG.baseURL}/auth/token/refresh/`,
      { refresh_token: refreshToken },
      {
        timeout: API_CONFIG.timeout as number,
        withCredentials: API_CONFIG.withCredentials,
      }
    )

    const { access_token } = response.data.data
    setToken(access_token)
    return access_token
  }

  /** 处理并发请求时的 Token 刷新，确保只刷新一次 */
  async handleRefresh(axiosInstance: AxiosInstance): Promise<string> {
    if (this.isRefreshing) {
      return new Promise((resolve, reject) => {
        this.refreshQueue.push({ resolve, reject })
      })
    }

    this.isRefreshing = true

    try {
      const newToken = await this.refreshToken(axiosInstance)
      this.refreshQueue.forEach(({ resolve }) => resolve(newToken))
      this.refreshQueue = []
      return newToken
    } catch (error) {
      this.refreshQueue.forEach(({ reject }) => reject(error))
      this.refreshQueue = []
      throw error
    } finally {
      this.isRefreshing = false
    }
  }

  /** 如有 refresh 正在进行则等待其完成 */
  async waitForRefreshIfNeeded(): Promise<string | null> {
    if (!this.isRefreshing) return null
    return new Promise((resolve, reject) => {
      this.refreshQueue.push({ resolve, reject })
    })
  }

  /** 清除 Token 并跳转登录页 */
  redirectToLogin(message = '登录已过期，请重新登录'): void {
    clearAllTokens()
    // ⚠️ 登录路由路径请按项目实际调整（当前模板登录页为 /signup_login）
    router.replace({ path: '/signup_login', query: { message } })
  }
}

export const tokenRefreshManager = new TokenRefreshManager()
