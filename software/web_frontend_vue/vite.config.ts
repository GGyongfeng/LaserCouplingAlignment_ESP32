import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  
  console.log('------------vite.config.ts--------------')
  console.log('构建信息:')
  console.log('当前模式:', mode)
  console.log('当前工作目录:', process.cwd())
  console.log('环境变量:')
  console.log('- VITE_APP_TITLE:', env.VITE_APP_TITLE)
  console.log('- VITE_APP_VERSION:', env.VITE_APP_VERSION)
  
  return {
    plugins: [
      vue()
    ],
    
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src')
      },
      extensions: ['.vue', '.ts', '.js']
    },
    
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
            @import "@/assets/styles/variables.scss";
          `
        }
      }
    },
    
    server: {
      port: Number(env.VITE_PORT) || 3000,
      host: true,
      proxy: {
        '/api': {
          target: env.VITE_BASE_API_URL || 'http://localhost:8080',
          changeOrigin: true,
        }
      }
    },
    
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: false,
      rollupOptions: {
        output: {
          assetFileNames: 'assets/[name].[hash].[ext]',
          chunkFileNames: 'assets/[name].[hash].js',
          entryFileNames: 'assets/[name].[hash].js',
        }
      }
    }
  }
})
