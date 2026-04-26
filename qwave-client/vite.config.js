import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  base: '/app/',
  plugins: [svelte()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:4269',
        rewrite: path => path.replace(/^\/api/, '')
      }
    }
  },
  build: {
    outDir: '../qwave-server/src/qwave/static/app'
  }
})
