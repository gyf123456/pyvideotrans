import client from './client'
import type { ApiResponse, UploadResponse } from '@/types/api'

export async function uploadFile(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await client.post<ApiResponse<UploadResponse>>('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 600000,
  })
  return res.data.data
}
