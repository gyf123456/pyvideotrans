import client from './client'
import type { ApiResponse } from '@/types/api'
import type { LanguageItem } from '@/types/provider'

export async function getLanguages() {
  const res = await client.get<ApiResponse<LanguageItem[]>>('/api/languages')
  return res.data.data
}
