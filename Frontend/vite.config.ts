import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  // dev server 代理目标：优先用专门的代理地址，回退到 API 基础地址
  const proxyTarget = env.VITE_PROXY_API_TARGET || env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

  return {
    plugins: [vue(), tailwindcss()],
    resolve: {
      alias: {
        '@': '/src',
      },
    },
    server: {
      proxy: {
        '/api': {
          target: proxyTarget,
          changeOrigin: true, // 需要代理跨域
          rewrite: path => path.replace(/^\/api/, ''), // 路径重写，把 '/api' 替换为 ''
        },
      },
    },
  }
})
