import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Icons from 'unplugin-icons/vite'
import { resolve } from 'path'

export default defineConfig({
  plugins: [
    vue(),
    Icons({
      compiler: 'vue3',
      autoInstall: true,
    }),
    // Custom plugin to resolve ~icons imports
    {
      name: 'resolve-icons',
      resolveId(id) {
        if (id.startsWith('~icons/')) {
          const parts = id.replace('~icons/', '').split('/')
          if (parts.length === 2) {
            const [collection, icon] = parts
            return resolve(__dirname, `node_modules/@iconify-json/${collection}/${icon}.json`)
          }
        }
        return null
      },
      load(id) {
        if (id.endsWith('.json') && id.includes('@iconify-json')) {
          // Return a Vue component that uses the icon data
          const fs = require('fs')
          const iconData = JSON.parse(fs.readFileSync(id, 'utf-8'))
          // This is a simplified version - unplugin-icons should handle the actual component generation
          return `export default ${JSON.stringify(iconData)}`
        }
        return null
      },
    },
  ],
  base: '/assets/all_trails/frontend/',
  build: {
    outDir: '../all_trails/public/frontend',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/app': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/assets': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
