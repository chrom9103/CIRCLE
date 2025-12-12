import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  base: '/CIRCLE/',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    // Docker コンテナ内でのホットリロード対応
    host: '0.0.0.0',
    port: 5173,
    watch: {
      // Docker のボリュームマウントでファイル変更を検知するために polling を使用
      usePolling: true,
      interval: 1000,
    },
    hmr: {
      // HMR (Hot Module Replacement) を有効化
      host: 'localhost',
      port: 5173,
    },
  },
})
