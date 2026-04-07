import client from './client'
import type { ApiResponse } from '@/types/api'
import type { SystemInfo } from '@/types/config'

export async function getSystemInfo() {
  const res = await client.get<ApiResponse<SystemInfo>>('/api/system/info')
  return res.data.data
}

export async function healthCheck() {
  const res = await client.get<ApiResponse<{ status: string }>>('/api/system/health')
  return res.data.data
}
