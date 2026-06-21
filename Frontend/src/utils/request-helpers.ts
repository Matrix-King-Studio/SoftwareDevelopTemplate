/** 生成请求唯一键（用于去重和缓存） */
export const generateRequestKey = (url: string, method: string, params?: unknown): string => {
  const paramsStr = params ? JSON.stringify(params) : ''
  return `${method.toUpperCase()}_${url}_${paramsStr}`
}

/** 生成链路追踪 ID（注入请求头 X-Trace-Id，便于前后端日志关联） */
export const generateTraceId = (): string => {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`
}
