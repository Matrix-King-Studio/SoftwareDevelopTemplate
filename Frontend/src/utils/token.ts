import { STORAGE_KEYS } from '@/config/api'
import { cacheManager } from '@/utils/request-cache'

/**
 * 保存 access token 到 localStorage
 * @param token - JWT access token 字符串
 */
export function setToken(token: string): void {
  localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token)
}

/**
 * 获取当前存储的 access token
 * @returns token 字符串，未登录时返回 null
 */
export function getToken(): string | null {
  return localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN)
}

/** 移除 access token */
export function removeToken(): void {
  localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN)
}

/**
 * 保存 refresh token 到 localStorage
 * @param token - JWT refresh token 字符串
 */
export function setRefreshToken(token: string): void {
  localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, token)
}

/**
 * 获取当前存储的 refresh token
 * @returns token 字符串，未登录时返回 null
 */
export function getRefreshToken(): string | null {
  return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)
}

/** 移除 refresh token */
export function removeRefreshToken(): void {
  localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
}

/** 清除所有 token 与缓存（登出时调用） */
export function clearAllTokens(): void {
  removeToken()
  removeRefreshToken()
  cacheManager.clear()
}
