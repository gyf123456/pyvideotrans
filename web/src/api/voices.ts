import client from './client'
import type { ApiResponse } from '@/types/api'
import type { VoiceItem } from '@/types/provider'

export async function getVoices(ttsType: number, language: string = '') {
  const res = await client.get<ApiResponse<VoiceItem[]>>('/api/voices', {
    params: { tts_type: ttsType, language },
  })
  return res.data.data
}
