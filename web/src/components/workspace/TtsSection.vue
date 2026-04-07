<template>
  <div class="tts-section">
    <h4>配音</h4>

    <el-form label-position="top" size="default">
      <el-form-item label="配音引擎">
        <el-select v-model="paramsStore.data.tts_type" class="full-width">
          <el-option
            v-for="item in providersStore.ttsList"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="配音角色">
        <div class="role-row">
          <el-select
            v-model="paramsStore.data.voice_role"
            class="role-select"
            filterable
            :loading="loadingVoices"
          >
            <el-option
              v-for="voice in voiceList"
              :key="voice.name"
              :label="voice.label || voice.name"
              :value="voice.name"
            />
          </el-select>
          <el-button
            :icon="isPlaying ? VideoPause : VideoPlay"
            :loading="previewing"
            :disabled="!paramsStore.data.voice_role || paramsStore.data.voice_role === 'No'"
            @click="handlePreview"
            circle
          />
        </div>
      </el-form-item>
    </el-form>

    <!-- Hidden audio element for playback -->
    <audio ref="audioRef" @ended="isPlaying = false" @error="isPlaying = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from 'vue'
import { VideoPlay, VideoPause } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useParamsStore } from '@/stores/params'
import { useProvidersStore } from '@/stores/providers'
import { getVoices } from '@/api/voices'
import client from '@/api/client'
import type { VoiceItem } from '@/types/provider'

const paramsStore = useParamsStore()
const providersStore = useProvidersStore()

const voiceList = ref<VoiceItem[]>([])
const loadingVoices = ref(false)
const previewing = ref(false)
const isPlaying = ref(false)
const audioRef = ref<HTMLAudioElement | null>(null)
let currentAudioUrl: string | null = null

watch(
  () => paramsStore.data.tts_type,
  async (ttsType) => {
    if (ttsType == null) return
    loadingVoices.value = true
    try {
      const lang = paramsStore.data.target_language || ''
      voiceList.value = await getVoices(ttsType, lang)
      const names = voiceList.value.map((v) => v.name)
      if (!names.includes(paramsStore.data.voice_role)) {
        paramsStore.data.voice_role = names.length ? names[0] : ''
      }
    } catch {
      voiceList.value = []
    } finally {
      loadingVoices.value = false
    }
  },
  { immediate: true }
)

async function handlePreview() {
  if (isPlaying.value) {
    // Stop current playback
    audioRef.value?.pause()
    isPlaying.value = false
    return
  }

  previewing.value = true
  try {
    const rate = Number(paramsStore.data.voice_rate ?? 0)
    const vol = Number(paramsStore.data.volume ?? 0)
    const pitch = Number(paramsStore.data.pitch ?? 0)

    const res = await client.post('/api/tts/preview', {
      tts_type: paramsStore.data.tts_type,
      voice_role: paramsStore.data.voice_role,
      language: paramsStore.data.target_language || 'zh-cn',
      voice_rate: rate >= 0 ? `+${rate}%` : `${rate}%`,
      volume: vol >= 0 ? `+${vol}%` : `${vol}%`,
      pitch: pitch >= 0 ? `+${pitch}Hz` : `${pitch}Hz`,
    }, { responseType: 'blob' })

    // Check if response is JSON error (ApiResponse with code != 0)
    const blob = res.data as Blob
    if (blob.type.includes('json')) {
      const text = await blob.text()
      const json = JSON.parse(text)
      ElMessage.error(json.msg || '试听失败')
      return
    }

    // Revoke previous URL
    if (currentAudioUrl) {
      URL.revokeObjectURL(currentAudioUrl)
    }

    currentAudioUrl = URL.createObjectURL(blob)
    if (audioRef.value) {
      audioRef.value.src = currentAudioUrl
      audioRef.value.play()
      isPlaying.value = true
    }
  } catch (e: any) {
    ElMessage.error(e?.message || '试听请求失败')
  } finally {
    previewing.value = false
  }
}

onBeforeUnmount(() => {
  audioRef.value?.pause()
  if (currentAudioUrl) {
    URL.revokeObjectURL(currentAudioUrl)
  }
})
</script>

<style scoped>
.tts-section {
  margin-bottom: 16px;
}

.full-width {
  width: 100%;
}

.role-row {
  display: flex;
  gap: 8px;
  width: 100%;
}

.role-select {
  flex: 1;
}
</style>
