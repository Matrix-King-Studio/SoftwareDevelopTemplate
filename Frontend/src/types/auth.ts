/**
 * 当前登录用户信息
 *
 * 字段为模板示例，请根据后端实际返回结构调整。
 */
export interface UserInfo {
  /** 用户 ID */
  id: number
  /** 用户名 */
  username: string
  /** 邮箱 */
  email?: string
  /** 头像地址 */
  avatar?: string
}

/**
 * 登录接口请求参数
 */
export interface LoginParams {
  username: string
  password: string
}

/**
 * 注册接口请求参数（贴合 dj-rest-auth 默认字段）
 */
export interface RegisterParams {
  username: string
  email: string
  password1: string
  password2: string
}

/**
 * 登录/刷新成功后的令牌载荷
 *
 * ⚠️ 后端契约：登录接口的 data 需返回 access_token + refresh_token + user。
 */
export interface AuthTokens {
  /** 访问令牌 */
  access_token: string
  /** 刷新令牌 */
  refresh_token: string
  /** 当前用户信息 */
  user: UserInfo
}

/**
 * 刷新令牌接口的 data 载荷
 */
export interface RefreshTokenResult {
  /** 新的访问令牌 */
  access_token: string
}
