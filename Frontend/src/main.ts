import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router/index'
import { useAccountStore } from './stores/account'
import { ensureCacheCleanupStarted } from './utils/request-cache'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

// 初始化认证状态（从 localStorage 恢复）
const accountStore = useAccountStore()
accountStore.initializeAuth()

// 启动 GET 请求缓存的定时清理
ensureCacheCleanupStarted()

app.use(router)
app.mount('#app')
