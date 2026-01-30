import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: "http://127.0.0.1:8000/",
        changeOrigin: true, //需要代理跨域
        rewrite: (path) => path.replace(/^\/api/, ''), //路径重写，把'/api'替换为''
      },
    },
  },
})
