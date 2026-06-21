/**
 * 当前登录用户信息
 *
 * 字段与后端 `Account/serializers/auth.py` 的 UserInfoSerializer 对齐,
 * 改动需前后端同步。
 */
export interface UserInfo {
  /** 用户 ID */
  id: number
  /** 用户名 */
  username: string
  /** 邮箱 */
  email?: string
  /** 业务角色：user=普通用户，admin=管理员 */
  role?: string
  /** 账号状态：active=启用，disabled=停用 */
  status?: string
  /** 头像地址 */
  avatar?: string
  /** 注册时间（ISO 字符串） */
  date_joined?: string
}

/**
 * 登录接口请求参数
 */
export interface LoginParams {
  username: string
  password: string
}

/**
 * 注册接口请求参数
 */
export interface RegisterParams {
  username: string
  email: string
  password1: string
  password2: string
}

/**
 * 登录/注册成功后的令牌载荷
 *
 * ⚠️ 后端契约：登录/注册接口的 data 返回 access_token + refresh_token + expires_in + user。
 */
export interface AuthTokens {
  /** 访问令牌 */
  access_token: string
  /** 刷新令牌 */
  refresh_token: string
  /** 访问令牌过期秒数 */
  expires_in: number
  /** 当前用户信息 */
  user: UserInfo
}

/**
 * 刷新令牌接口的 data 载荷
 */
export interface RefreshTokenResult {
  /** 新的访问令牌 */
  access_token: string
  /** 访问令牌过期秒数 */
  expires_in?: number
}
