import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// GitHub Pages: https://alexbyyao.github.io/AI-Articles/
export default defineConfig({
  plugins: [vue()],
  base: '/AI-Articles/',
})
