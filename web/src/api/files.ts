import client from './client'
import type { ApiResponse } from '@/types/api'
import type { FileItem } from '@/types/config'

export async function listFiles(taskId?: string) {
  const res = await client.get<ApiResponse<FileItem[]>>('/api/files', {
    params: taskId ? { task_id: taskId } : {},
  })
  return res.data.data
}

export function getDownloadUrl(path: string) {
  const base = import.meta.env.VITE_API_BASE || ''
  return `${base}/api/files/download?path=${encodeURIComponent(path)}`
}
