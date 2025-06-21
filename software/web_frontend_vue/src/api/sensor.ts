import axios from 'axios'

// 基础配置
console.log('当前环境变量VITE_BASE_API_URL:', import.meta.env.VITE_BASE_API_URL)
const baseURL = import.meta.env.VITE_BASE_API_URL || 'http://localhost:8080'
console.log('最终请求地址:', baseURL)

const api = axios.create({
  baseURL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 传感器测量接口
import type { SensorResponse } from '@/types/sensor'

// 更新响应数据类型（已通过view_files确认SensorResponse结构正确）

export const measureSensors = () => {
  console.log('正在请求传感器接口，路径:', '/getdistance')
  return api.get<SensorResponse>('/getdistance').then(res => {
    console.log('传感器接口响应:', res)
    return res
  }).catch(err => {
    console.error('传感器接口请求异常:', err)
    throw err
  })
}

// 响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)