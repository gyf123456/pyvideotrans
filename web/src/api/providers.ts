import client from './client'
import type { ApiResponse } from '@/types/api'
import type { ProviderItem } from '@/types/provider'

export async function getProviders(type: 'recognition' | 'translation' | 'tts') {
  const res = await client.get<ApiResponse<ProviderItem[]>>(`/api/providers/${type}`)
  return res.data.data
}
