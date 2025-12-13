import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Use VITE_API_URL for dev proxy if provided, fallback to localhost
const API_TARGET = process.env.VITE_API_URL || 'http://localhost:8000';

// https://vite.dev/config/
export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? '/JOSNISHOP_000/' : '/',
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: API_TARGET,
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
