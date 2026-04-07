export interface ApiResponse<T = any> {
  code: number
  msg: string
  data: T
}

export interface UploadResponse {
  filepath: string
}

export interface TaskCreateRequest {
  task: 'stt' | 'tts' | 'sts' | 'vtv'
  name: string
  // STT params
  recogn_type?: number
  detect_language?: string
  model_name?: string
  is_cuda?: boolean
  remove_noise?: boolean
  enable_diariz?: boolean
  nums_diariz?: number
  rephrase?: number
  fix_punc?: boolean
  // TTS params
  tts_type?: number
  voice_role?: string
  voice_rate?: string
  volume?: string
  pitch?: string
  voice_autorate?: boolean
  video_autorate?: boolean
  align_sub_audio?: boolean
  target_language_code?: string
  // STS params
  translate_type?: number
  source_language_code?: string
  // VTV params
  is_separate?: boolean
  recogn2pass?: boolean
  subtitle_type?: number
  clear_cache?: boolean
}

export interface TaskCreateResponse {
  task_id: string
  target_dir: string
}

export interface ConfigUpdateRequest {
  data: Record<string, any>
}
