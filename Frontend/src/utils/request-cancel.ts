import { generateRequestKey } from '@/utils/request-helpers'
import type { DedupStrategy } from '@/api/core/request-config'

/**
 * 请求去重 / 取消管理器
 *
 * 基于 AbortController，对“相同 URL + method + 参数”的请求做去重：
 * - cancel-old：取消旧请求，发送新请求（默认，适合搜索联想等场景）
 * - reject-new：已有相同请求进行中时，拒绝新请求（适合防止表单重复提交）
 */
class CancelManager {
  private pendingRequests = new Map<string, AbortController>()

  /** 添加请求，根据策略决定取消旧请求或拒绝新请求 */
  addPendingRequest(
    url: string,
    method: string,
    params?: unknown,
    strategy: DedupStrategy = 'cancel-old'
  ): AbortController {
    const requestKey = generateRequestKey(url, method, params)

    if (strategy === 'reject-new' && this.pendingRequests.has(requestKey)) {
      // reject-new：已有相同请求则中止新请求
      const controller = new AbortController()
      controller.abort('请求已取消：重复请求（reject-new）')
      return controller
    }

    // cancel-old：取消旧请求，发新请求
    this.removePendingRequest(requestKey)

    const controller = new AbortController()
    this.pendingRequests.set(requestKey, controller)
    return controller
  }

  /** 取消并移除指定请求 */
  removePendingRequest(requestKey: string): void {
    const controller = this.pendingRequests.get(requestKey)
    if (controller) {
      controller.abort('请求已取消：重复请求')
      this.pendingRequests.delete(requestKey)
    }
  }

  /** 取消所有请求（路由切换时调用） */
  cancelAllRequests(reason = '页面切换，取消所有请求'): void {
    this.pendingRequests.forEach(controller => {
      controller.abort(reason)
    })
    this.pendingRequests.clear()
  }

  /** 清理已完成的请求 */
  clearRequest(url: string, method: string, params?: unknown): void {
    const requestKey = generateRequestKey(url, method, params)
    this.pendingRequests.delete(requestKey)
  }

  /** 检查请求是否正在进行 */
  isPending(url: string, method: string, params?: unknown): boolean {
    const requestKey = generateRequestKey(url, method, params)
    return this.pendingRequests.has(requestKey)
  }
}

export const cancelManager = new CancelManager()
