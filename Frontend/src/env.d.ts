/// <reference types="vite/client" />

/** 环境变量类型声明（与 .env.* 文件中的 VITE_ 变量一一对应） */
interface ImportMetaEnv {
  /** 应用标题 */
  readonly VITE_APP_TITLE: string
  /** 后端 API 基础地址：开发环境为 /api，生产/测试环境为绝对域名或 /api */
  readonly VITE_API_BASE_URL: string
  /** 仅 vite dev server 使用的本地代理目标（后端实际监听地址） */
  readonly VITE_PROXY_API_TARGET?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

/** .vue 单文件组件模块声明 */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>
  export default component
}
