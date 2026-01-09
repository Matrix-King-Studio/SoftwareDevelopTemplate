import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router/index'
import { useAccountStore } from './stores/account'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

// 初始化认证状态（从localStorage恢复）
const accountStore = useAccountStore()
accountStore.initializeAuth()

app.use(router)
app.mount('#app')
