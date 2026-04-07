import axios from 'axios'
import type { ApiResponse } from '@/types/api'
import { ElMessage } from 'element-plus'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 30000,
})

client.interceptors.response.use(
  (response) => {
    const data = response.data as ApiResponse
    if (data.code !== 0) {
      ElMessage.error(data.msg || 'Request failed')
      return Promise.reject(new Error(data.msg))
    }
    return response
  },
  (error) => {
    const msg = error.response?.data?.detail || error.message || 'Network error'
    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

export default client
