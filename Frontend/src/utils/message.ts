import { ElMessage, type MessageOptions } from 'element-plus'

type MessageContent = NonNullable<MessageOptions['message']>

/** 统一消息提示配置，避免各页面重复设置 Element Plus Message 行为 */
const baseMessageOptions = {
  duration: 3000,
  grouping: true,
} satisfies Partial<MessageOptions>

/** 全局消息提示方法集合 */
export const message = {
  /** 展示成功反馈 */
  success(content: MessageContent) {
    return ElMessage.success({ ...baseMessageOptions, message: content })
  },

  /** 展示错误反馈 */
  error(content: MessageContent) {
    return ElMessage.error({ ...baseMessageOptions, message: content })
  },

  /** 展示警告反馈 */
  warning(content: MessageContent) {
    return ElMessage.warning({ ...baseMessageOptions, message: content })
  },

  /** 展示普通信息反馈 */
  info(content: MessageContent) {
    return ElMessage.info({ ...baseMessageOptions, message: content })
  },
}

/**
 * 从接口异常中提取适合展示给用户的提示文案。
 * @param error 接口调用抛出的异常对象，可为 ApiError 或其他 Error
 * @param fallback 当异常对象中没有可用 message 时展示的兜底文案
 * @returns 优先返回异常 message，否则返回兜底文案
 */
export function getFeedbackMessage(error: unknown, fallback: string): string {
  return error instanceof Error && error.message ? error.message : fallback
}
