import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import * as accountApi from '@/api/modules/account'
import { getToken, setToken, setRefreshToken, clearAllTokens } from '@/utils/token'
import { getFeedbackMessage } from '@/utils/message'
import type { UserInfo } from '@/types/auth'

/** 本地存储中保存用户信息的键名（token 由 utils/token.ts 统一管理） */
const STORAGE_KEY_USER = 'auth_user'

/**
 * 账户状态管理
 *
 * 对外方法签名保持稳定，登录组件无需感知底层认证细节。
 * 认证采用 JWT Bearer + 刷新令牌方案（见 api/modules/account.ts 的后端契约说明）。
 */
export const useAccountStore = defineStore('account', () => {
  /** 当前登录用户信息 */
  const userInfo = ref<UserInfo | null>(null)
  /** 访问令牌（来源于 localStorage，便于模板内引用） */
  const token = ref<string | null>(null)
  /** 请求进行中标志 */
  const isLoading = ref<boolean>(false)
  /** 最近一次错误信息 */
  const error = ref<string | null>(null)

  /** 是否已登录 */
  const isLoggedIn = computed(() => !!userInfo.value)

  /** 初始化：从 localStorage 恢复登录状态 */
  const initializeAuth = () => {
    try {
      const savedToken = getToken()
      const savedUser = localStorage.getItem(STORAGE_KEY_USER)

      if (savedToken && savedUser) {
        token.value = savedToken
        userInfo.value = JSON.parse(savedUser) as UserInfo
      }
    } catch (err) {
      console.error('恢复登录状态失败:', err)
      clearAuthState()
    }
  }

  /** 保存登录状态（access/refresh token + 用户信息） */
  const saveAuthState = (accessToken: string, refreshToken: string, newUserInfo: UserInfo) => {
    setToken(accessToken)
    setRefreshToken(refreshToken)
    token.value = accessToken
    userInfo.value = newUserInfo
    localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(newUserInfo))
  }

  /** 清除登录状态 */
  const clearAuthState = () => {
    clearAllTokens()
    token.value = null
    userInfo.value = null
    localStorage.removeItem(STORAGE_KEY_USER)
  }

  /**
   * 登录
   * @returns `{ success, data }` 或 `{ success, error }`
   */
  const login = async (username: string, password: string) => {
    isLoading.value = true
    error.value = null

    try {
      const res = await accountApi.login({ username, password })
      const { access_token, refresh_token, user } = res.data
      saveAuthState(access_token, refresh_token, user)
      return { success: true, data: res.data }
    } catch (err: unknown) {
      const msg = getFeedbackMessage(err, '登录失败')
      error.value = msg
      return { success: false, error: msg }
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 注册
   * @returns `{ success, data }` 或 `{ success, error }`
   */
  const register = async (
    username: string,
    email: string,
    password1: string,
    password2: string
  ) => {
    isLoading.value = true
    error.value = null

    try {
      const res = await accountApi.register({ username, email, password1, password2 })
      return { success: true, data: res.data }
    } catch (err: unknown) {
      const msg = getFeedbackMessage(err, '注册失败')
      error.value = msg
      return { success: false, error: msg }
    } finally {
      isLoading.value = false
    }
  }

  /** 登出：调用后端登出接口（失败忽略），并清除本地状态 */
  const logout = async () => {
    try {
      await accountApi.logout()
    } catch {
      // 后端登出失败不阻断前端登出
    } finally {
      clearAuthState()
    }
  }

  /** 拉取当前用户信息并刷新本地缓存 */
  const fetchUserInfo = async () => {
    try {
      const res = await accountApi.getCurrentUser()
      userInfo.value = res.data
      localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(res.data))
      return { success: true, data: res.data }
    } catch (err: unknown) {
      const msg = getFeedbackMessage(err, '获取用户信息失败')
      error.value = msg
      return { success: false, error: msg }
    }
  }

  return {
    userInfo,
    token,
    isLoading,
    error,
    isLoggedIn,
    login,
    register,
    logout,
    fetchUserInfo,
    initializeAuth,
  }
})
