import client from './client'
import type { ApiResponse } from '@/types/api'
import type { Settings, Params } from '@/types/config'

export async function getSettings() {
  const res = await client.get<ApiResponse<Settings>>('/api/config/settings')
  return res.data.data
}

export async function updateSettings(data: Record<string, any>) {
  const res = await client.put<ApiResponse<Settings>>('/api/config/settings', { data })
  return res.data.data
}

export async function getParams() {
  const res = await client.get<ApiResponse<Params>>('/api/config/params')
  return res.data.data
}

export async function updateParams(data: Record<string, any>) {
  const res = await client.put<ApiResponse<Params>>('/api/config/params', { data })
  return res.data.data
}
