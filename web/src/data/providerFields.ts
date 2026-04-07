export interface ProviderFieldDef {
  key: string
  label: string
  type: 'text' | 'password' | 'select' | 'models_editor' | 'textarea' | 'number' | 'slider' | 'checkbox'
  settingsKey?: string
  placeholder?: string
  min?: number
  max?: number
  step?: number
  options?: { label: string; value: any }[]
}

export interface ProviderConfig {
  id: string
  title: string
  category: 'translation' | 'tts' | 'recognition'
  fields: ProviderFieldDef[]
}

export const PROVIDER_CONFIGS: Record<string, ProviderConfig> = {
  // --- Translation Providers ---
  chatgpt: {
    id: 'chatgpt',
    title: 'OpenAI ChatGPT',
    category: 'translation',
    fields: [
      { key: 'chatgpt_api', label: 'API URL', type: 'text', placeholder: 'https://api.openai.com' },
      { key: 'chatgpt_key', label: 'API Key', type: 'password' },
      { key: 'chatgpt_model', label: 'Model', type: 'select', settingsKey: 'chatgpt_model' },
      { key: 'chatgpt_max_token', label: 'Max Tokens', type: 'text', placeholder: '8192' },
    ],
  },
  claude: {
    id: 'claude',
    title: 'Claude AI',
    category: 'translation',
    fields: [
      { key: 'claude_api', label: 'API URL', type: 'text', placeholder: 'https://api.anthropic.com' },
      { key: 'claude_key', label: 'API Key', type: 'password' },
      { key: 'claude_model', label: 'Model', type: 'text', placeholder: 'claude-sonnet-4-20250514' },
    ],
  },
  azure: {
    id: 'azure',
    title: 'Azure OpenAI',
    category: 'translation',
    fields: [
      { key: 'azure_api', label: 'API URL', type: 'text' },
      { key: 'azure_key', label: 'API Key', type: 'password' },
      { key: 'azure_model', label: 'Model', type: 'select', settingsKey: 'azure_model' },
      { key: 'azure_version', label: 'API Version', type: 'text', placeholder: '2025-04-01-preview' },
    ],
  },
  gemini: {
    id: 'gemini',
    title: 'Google Gemini',
    category: 'translation',
    fields: [
      { key: 'gemini_key', label: 'API Key', type: 'password' },
      { key: 'gemini_model', label: 'Model', type: 'select', settingsKey: 'gemini_model' },
      { key: 'gemini_maxtoken', label: 'Max Tokens', type: 'number', min: 1, max: 100000 },
    ],
  },
  deepseek: {
    id: 'deepseek',
    title: 'DeepSeek',
    category: 'translation',
    fields: [
      { key: 'deepseek_key', label: 'API Key', type: 'password' },
      { key: 'deepseek_model', label: 'Model', type: 'select', settingsKey: 'deepseek_model' },
      { key: 'deepseek_max_token', label: 'Max Tokens', type: 'text', placeholder: '8192' },
    ],
  },
  localllm: {
    id: 'localllm',
    title: 'Local LLM (OpenAI-compatible)',
    category: 'translation',
    fields: [
      { key: 'localllm_api', label: 'API URL', type: 'text', placeholder: 'http://127.0.0.1:11434/v1' },
      { key: 'localllm_key', label: 'API Key', type: 'password' },
      { key: 'localllm_model', label: 'Model', type: 'select', settingsKey: 'localllm_model' },
      { key: 'localllm_max_token', label: 'Max Tokens', type: 'text', placeholder: '4096' },
    ],
  },
  zhipu: {
    id: 'zhipu',
    title: 'Zhipu AI (GLM)',
    category: 'translation',
    fields: [
      { key: 'zhipu_key', label: 'API Key', type: 'password' },
      { key: 'zhipu_model', label: 'Model', type: 'select', settingsKey: 'zhipuai_model' },
      { key: 'zhipu_max_token', label: 'Max Tokens', type: 'text', placeholder: '98304' },
    ],
  },
  openrouter: {
    id: 'openrouter',
    title: 'OpenRouter',
    category: 'translation',
    fields: [
      { key: 'openrouter_key', label: 'API Key', type: 'password' },
      { key: 'openrouter_model', label: 'Model', type: 'select', settingsKey: 'openrouter_model' },
      { key: 'openrouter_max_token', label: 'Max Tokens', type: 'text', placeholder: '8192' },
    ],
  },
  guiji: {
    id: 'guiji',
    title: 'SiliconFlow',
    category: 'translation',
    fields: [
      { key: 'guiji_key', label: 'API Key', type: 'password' },
      { key: 'guiji_model', label: 'Model', type: 'select', settingsKey: 'guiji_model' },
      { key: 'guiji_max_token', label: 'Max Tokens', type: 'text', placeholder: '8192' },
    ],
  },
  zijiehuoshan: {
    id: 'zijiehuoshan',
    title: 'VolcEngine LLM',
    category: 'translation',
    fields: [
      { key: 'zijiehuoshan_key', label: 'API Key', type: 'password' },
      { key: 'zijiehuoshan_model', label: 'Model', type: 'select', settingsKey: 'zijiehuoshan_model' },
    ],
  },
  ai302: {
    id: 'ai302',
    title: '302.AI',
    category: 'translation',
    fields: [
      { key: 'ai302_key', label: 'API Key', type: 'password' },
      { key: 'ai302_model', label: 'Model', type: 'select', settingsKey: 'ai302_models' },
    ],
  },
  deepl: {
    id: 'deepl',
    title: 'DeepL',
    category: 'translation',
    fields: [
      { key: 'deepl_authkey', label: 'Auth Key', type: 'password' },
      { key: 'deepl_api', label: 'API URL', type: 'text', placeholder: 'https://api-free.deepl.com' },
      { key: 'deepl_gid', label: 'Glossary ID', type: 'text' },
    ],
  },
  deeplx: {
    id: 'deeplx',
    title: 'DeepLx',
    category: 'translation',
    fields: [
      { key: 'deeplx_address', label: 'API URL', type: 'text' },
      { key: 'deeplx_key', label: 'Key', type: 'password' },
    ],
  },
  baidu: {
    id: 'baidu',
    title: 'Baidu Translation',
    category: 'translation',
    fields: [
      { key: 'baidu_appid', label: 'APP ID', type: 'text' },
      { key: 'baidu_miyue', label: 'Secret Key', type: 'password' },
    ],
  },
  tencent: {
    id: 'tencent',
    title: 'Tencent Translation',
    category: 'translation',
    fields: [
      { key: 'tencent_SecretId', label: 'Secret ID', type: 'text' },
      { key: 'tencent_SecretKey', label: 'Secret Key', type: 'password' },
    ],
  },
  libre: {
    id: 'libre',
    title: 'LibreTranslate',
    category: 'translation',
    fields: [
      { key: 'libre_address', label: 'API URL', type: 'text' },
      { key: 'libre_key', label: 'API Key', type: 'password' },
    ],
  },
  ott: {
    id: 'ott',
    title: 'OTT Translation',
    category: 'translation',
    fields: [
      { key: 'ott_address', label: 'API URL', type: 'text' },
    ],
  },
  trans_api: {
    id: 'trans_api',
    title: 'Custom Translation API',
    category: 'translation',
    fields: [
      { key: 'trans_api_url', label: 'API URL', type: 'text' },
      { key: 'trans_secret', label: 'Secret', type: 'password' },
    ],
  },
  qwenmt: {
    id: 'qwenmt',
    title: 'Ali-Bailian (Qwen-MT)',
    category: 'translation',
    fields: [
      { key: 'qwenmt_key', label: 'API Key', type: 'password' },
      { key: 'qwenmt_model', label: 'Model', type: 'text', placeholder: 'qwen-mt-turbo' },
      { key: 'qwenmt_domains', label: 'Domains', type: 'text' },
    ],
  },
  minimax: {
    id: 'minimax',
    title: 'MiniMax AI',
    category: 'translation',
    fields: [
      { key: 'minimax_key', label: 'API Key', type: 'password' },
      { key: 'minimax_model', label: 'Model', type: 'text', placeholder: 'MiniMax-M2.7' },
      { key: 'minimax_api', label: 'API URL', type: 'text', placeholder: 'https://api.minimaxi.com/v1' },
      { key: 'minimax_max_tokens', label: 'Max Tokens', type: 'number', min: 1, max: 100000 },
    ],
  },

  // --- TTS Providers ---
  openaitts: {
    id: 'openaitts',
    title: 'OpenAI TTS',
    category: 'tts',
    fields: [
      { key: 'openaitts_api', label: 'API URL', type: 'text' },
      { key: 'openaitts_key', label: 'API Key', type: 'password' },
      { key: 'openaitts_model', label: 'Model', type: 'select', settingsKey: 'openaitts_model' },
      { key: 'openaitts_role', label: 'Voice Role', type: 'text' },
      { key: 'openaitts_instructions', label: 'Instructions', type: 'textarea' },
    ],
  },
  elevenlabs: {
    id: 'elevenlabs',
    title: 'ElevenLabs TTS',
    category: 'tts',
    fields: [
      { key: 'elevenlabstts_key', label: 'API Key', type: 'password' },
      { key: 'elevenlabstts_models', label: 'Model', type: 'text', placeholder: 'eleven_flash_v2_5' },
    ],
  },
  azure_speech: {
    id: 'azure_speech',
    title: 'Azure TTS',
    category: 'tts',
    fields: [
      { key: 'azure_speech_region', label: 'Region', type: 'text' },
      { key: 'azure_speech_key', label: 'API Key', type: 'password' },
    ],
  },
  gemini_tts: {
    id: 'gemini_tts',
    title: 'Gemini TTS',
    category: 'tts',
    fields: [
      { key: 'gemini_key', label: 'API Key', type: 'password' },
      { key: 'gemini_ttsmodel', label: 'Model', type: 'text', placeholder: 'gemini-2.5-flash-preview-tts' },
      { key: 'gemini_ttsstyle', label: 'Style', type: 'text' },
    ],
  },
  xaitts: {
    id: 'xaitts',
    title: 'X.AI TTS',
    category: 'tts',
    fields: [
      { key: 'xaitts_key', label: 'API Key', type: 'password' },
    ],
  },
  qwentts: {
    id: 'qwentts',
    title: 'Qwen3-TTS (Bailian API)',
    category: 'tts',
    fields: [
      { key: 'qwentts_key', label: 'API Key', type: 'password' },
      { key: 'qwentts_model', label: 'Model', type: 'text', placeholder: 'qwen-tts-latest' },
      { key: 'qwentts_role', label: 'Voice Role', type: 'text', placeholder: 'Chelsie' },
    ],
  },
  qwenttslocal: {
    id: 'qwenttslocal',
    title: 'Qwen3-TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'qwenttslocal_url', label: 'API URL', type: 'text' },
      { key: 'qwenttslocal_refaudio', label: 'Reference Audio', type: 'text' },
      { key: 'qwenttslocal_prompt', label: 'Prompt', type: 'textarea' },
    ],
  },
  minimaxi_tts: {
    id: 'minimaxi_tts',
    title: 'MiniMaxi TTS',
    category: 'tts',
    fields: [
      { key: 'minimaxi_apikey', label: 'API Key', type: 'password' },
      { key: 'minimaxi_apiurl', label: 'API URL', type: 'text', placeholder: 'api.minimaxi.com' },
      { key: 'minimaxi_model', label: 'Model', type: 'text', placeholder: 'speech-02-turbo' },
      { key: 'minimaxi_emotion', label: 'Emotion', type: 'text' },
    ],
  },
  gptsovits: {
    id: 'gptsovits',
    title: 'GPT-SoVITS (Local)',
    category: 'tts',
    fields: [
      { key: 'gptsovits_url', label: 'API URL', type: 'text' },
      { key: 'gptsovits_role', label: 'Voice Role', type: 'text' },
      { key: 'gptsovits_isv2', label: 'V2 Mode', type: 'checkbox' },
      { key: 'gptsovits_extra', label: 'Extra Params', type: 'text' },
    ],
  },
  cosyvoice: {
    id: 'cosyvoice',
    title: 'CosyVoice (Local)',
    category: 'tts',
    fields: [
      { key: 'cosyvoice_url', label: 'API URL', type: 'text' },
      { key: 'cosyvoice_role', label: 'Voice Role', type: 'text' },
    ],
  },
  f5tts: {
    id: 'f5tts',
    title: 'F5-TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'f5tts_url', label: 'API URL', type: 'text' },
      { key: 'f5tts_model', label: 'Model', type: 'text' },
      { key: 'f5tts_ttstype', label: 'TTS Type', type: 'text', placeholder: 'F5-TTS' },
      { key: 'f5tts_role', label: 'Voice Role', type: 'text' },
    ],
  },
  chattts: {
    id: 'chattts',
    title: 'ChatTTS (Local)',
    category: 'tts',
    fields: [
      { key: 'chattts_api', label: 'API URL', type: 'text' },
    ],
  },
  kokoro: {
    id: 'kokoro',
    title: 'Kokoro TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'kokoro_api', label: 'API URL', type: 'text' },
    ],
  },
  doubao2: {
    id: 'doubao2',
    title: 'DouBao2 TTS',
    category: 'tts',
    fields: [
      { key: 'doubao2_appid', label: 'APP ID', type: 'text' },
      { key: 'doubao2_access', label: 'Access Token', type: 'password' },
    ],
  },
  volcenginetts: {
    id: 'volcenginetts',
    title: 'VolcEngine TTS',
    category: 'tts',
    fields: [
      { key: 'volcenginetts_appid', label: 'APP ID', type: 'text' },
      { key: 'volcenginetts_access', label: 'Access Token', type: 'password' },
      { key: 'volcenginetts_cluster', label: 'Cluster', type: 'text' },
    ],
  },
  gcloud_tts: {
    id: 'gcloud_tts',
    title: 'Google Cloud TTS',
    category: 'tts',
    fields: [
      { key: 'gcloud_credential_json', label: 'Credential JSON Path', type: 'text' },
      { key: 'gcloud_language_code', label: 'Language Code', type: 'text' },
      { key: 'gcloud_voice_name', label: 'Voice Name', type: 'text' },
      { key: 'gcloud_audio_encoding', label: 'Audio Encoding', type: 'text' },
      { key: 'gcloud_ssml_gender', label: 'SSML Gender', type: 'text' },
    ],
  },
  fishtts: {
    id: 'fishtts',
    title: 'Fish TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'fishtts_url', label: 'API URL', type: 'text' },
      { key: 'fishtts_role', label: 'Voice Role', type: 'text' },
    ],
  },
  clone: {
    id: 'clone',
    title: 'Clone Voice (Local)',
    category: 'tts',
    fields: [
      { key: 'clone_api', label: 'API URL', type: 'text' },
    ],
  },
  indextts: {
    id: 'indextts',
    title: 'Index TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'indextts_url', label: 'API URL', type: 'text' },
      { key: 'index_tts_version', label: 'Version', type: 'number', min: 1, max: 2 },
    ],
  },
  sparktts: {
    id: 'sparktts',
    title: 'Spark TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'sparktts_url', label: 'API URL', type: 'text' },
    ],
  },
  diatts: {
    id: 'diatts',
    title: 'Dia TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'diatts_url', label: 'API URL', type: 'text' },
    ],
  },
  voxcpmtts: {
    id: 'voxcpmtts',
    title: 'VoxCPM TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'voxcpmtts_url', label: 'API URL', type: 'text' },
    ],
  },
  chatterbox: {
    id: 'chatterbox',
    title: 'ChatterBox TTS (Local)',
    category: 'tts',
    fields: [
      { key: 'chatterbox_url', label: 'API URL', type: 'text' },
      { key: 'chatterbox_role', label: 'Voice Role', type: 'text' },
      { key: 'chatterbox_cfg_weight', label: 'CFG Weight', type: 'slider', min: 0, max: 1, step: 0.1 },
      { key: 'chatterbox_exaggeration', label: 'Exaggeration', type: 'slider', min: 0, max: 1, step: 0.1 },
    ],
  },
  ai302tts: {
    id: 'ai302tts',
    title: '302.AI TTS',
    category: 'tts',
    fields: [
      { key: 'ai302tts_key', label: 'API Key', type: 'password' },
      { key: 'ai302tts_model', label: 'Model', type: 'text' },
    ],
  },
  ttsapi: {
    id: 'ttsapi',
    title: 'Custom TTS API',
    category: 'tts',
    fields: [
      { key: 'ttsapi_url', label: 'API URL', type: 'text' },
      { key: 'ttsapi_voice_role', label: 'Voice Role', type: 'text' },
      { key: 'ttsapi_extra', label: 'Extra Params', type: 'text' },
    ],
  },

  // --- Recognition Providers ---
  openairecognapi: {
    id: 'openairecognapi',
    title: 'OpenAI Speech to Text',
    category: 'recognition',
    fields: [
      { key: 'openairecognapi_url', label: 'API URL', type: 'text' },
      { key: 'openairecognapi_key', label: 'API Key', type: 'password' },
      { key: 'openairecognapi_model', label: 'Model', type: 'select', settingsKey: 'openairecognapi_model' },
      { key: 'openairecognapi_prompt', label: 'Prompt', type: 'textarea' },
    ],
  },
  deepgram: {
    id: 'deepgram',
    title: 'Deepgram',
    category: 'recognition',
    fields: [
      { key: 'deepgram_apikey', label: 'API Key', type: 'password' },
    ],
  },
  whipserx: {
    id: 'whipserx',
    title: 'WhisperX API',
    category: 'recognition',
    fields: [
      { key: 'whipserx_api', label: 'API URL', type: 'text', placeholder: 'http://127.0.0.1:9092' },
    ],
  },
  stt: {
    id: 'stt',
    title: 'STT Speech API',
    category: 'recognition',
    fields: [
      { key: 'stt_url', label: 'API URL', type: 'text' },
      { key: 'stt_model', label: 'Model', type: 'text', placeholder: 'large-v3-turbo' },
    ],
  },
  recognapi: {
    id: 'recognapi',
    title: 'Custom Recognition API',
    category: 'recognition',
    fields: [
      { key: 'recognapi_url', label: 'API URL', type: 'text' },
      { key: 'recognapi_key', label: 'API Key', type: 'password' },
    ],
  },
  qwenmt_asr: {
    id: 'qwenmt_asr',
    title: 'Ali Qwen3-ASR',
    category: 'recognition',
    fields: [
      { key: 'qwenmt_key', label: 'API Key', type: 'password' },
      { key: 'qwenmt_asr_model', label: 'Model', type: 'text', placeholder: 'qwen3-asr-flash' },
    ],
  },
  zijierecognmodel: {
    id: 'zijierecognmodel',
    title: 'VolcEngine STT',
    category: 'recognition',
    fields: [
      { key: 'zijierecognmodel_appid', label: 'APP ID', type: 'text' },
      { key: 'zijierecognmodel_token', label: 'Token', type: 'password' },
    ],
  },
  ai302_recogn: {
    id: 'ai302_recogn',
    title: '302.AI Recognition',
    category: 'recognition',
    fields: [
      { key: 'ai302_key', label: 'API Key', type: 'password' },
      { key: 'ai302_model_recogn', label: 'Model', type: 'text', placeholder: 'whisper-1' },
    ],
  },
}
