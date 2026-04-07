<template>
  <el-tabs v-model="activeTab" type="border-card">
    <!-- Tab 1: General -->
    <el-tab-pane label="通用" name="general">
      <el-form label-position="top" :model="settingsStore.data">
        <el-form-item label="输出目录">
          <el-input
            :model-value="settingsStore.get('homedir')"
            @change="(v: string) => saveField('homedir', v)"
          />
        </el-form-item>
        <el-form-item label="代理">
          <el-input
            :model-value="settingsStore.get('proxy')"
            placeholder="http://127.0.0.1:7890"
            @change="(v: string) => saveField('proxy', v)"
          />
        </el-form-item>
        <el-form-item label="语言">
          <el-select
            :model-value="settingsStore.get('lang', 'en')"
            style="width: 100%"
            @change="(v: string) => saveField('lang', v)"
          >
            <el-option label="English" value="en" />
            <el-option label="简体中文" value="zh-cn" />
          </el-select>
        </el-form-item>
        <el-form-item label="视频编码">
          <el-select
            :model-value="settingsStore.get('video_codec', '264')"
            style="width: 100%"
            @change="(v: string) => saveField('video_codec', v)"
          >
            <el-option label="H.264" value="264" />
            <el-option label="H.265" value="265" />
          </el-select>
        </el-form-item>
        <el-form-item label="CRF">
          <el-input-number
            :model-value="settingsStore.get('crf', 13)"
            :min="0"
            :max="51"
            controls-position="right"
            @change="(v: number) => saveField('crf', v)"
          />
        </el-form-item>
        <el-form-item label="编码预设">
          <el-select
            :model-value="settingsStore.get('preset', 'medium')"
            style="width: 100%"
            @change="(v: string) => saveField('preset', v)"
          >
            <el-option
              v-for="p in presets"
              :key="p"
              :label="p"
              :value="p"
            />
          </el-select>
        </el-form-item>
      </el-form>
    </el-tab-pane>

    <!-- Tab 2: Speech Recognition -->
    <el-tab-pane label="语音识别" name="recognition">
      <el-form label-position="top" :model="settingsStore.data">
        <el-form-item label="Whisper模型">
          <el-input
            type="textarea"
            :rows="3"
            :model-value="settingsStore.get('model_list')"
            placeholder="tiny,base,small,medium,large-v3"
            @change="(v: string) => saveField('model_list', v)"
          />
        </el-form-item>
        <el-form-item label="计算类型">
          <el-select
            :model-value="settingsStore.get('cuda_com_type', 'default')"
            style="width: 100%"
            @change="(v: string) => saveField('cuda_com_type', v)"
          >
            <el-option
              v-for="opt in cudaComTypes"
              :key="opt"
              :label="opt"
              :value="opt"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="VAD类型">
          <el-select
            :model-value="settingsStore.get('vad_type', 'tenvad')"
            style="width: 100%"
            @change="(v: string) => saveField('vad_type', v)"
          >
            <el-option label="tenvad" value="tenvad" />
            <el-option label="silero" value="silero" />
          </el-select>
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="beam_size">
              <el-input-number
                :model-value="settingsStore.get('beam_size', 5)"
                :min="1"
                :max="20"
                controls-position="right"
                @change="(v: number) => saveField('beam_size', v)"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="best_of">
              <el-input-number
                :model-value="settingsStore.get('best_of', 5)"
                :min="1"
                :max="20"
                controls-position="right"
                @change="(v: number) => saveField('best_of', v)"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="threshold">
              <el-input-number
                :model-value="settingsStore.get('threshold', 0.5)"
                :min="0"
                :max="1"
                :step="0.05"
                controls-position="right"
                @change="(v: number) => saveField('threshold', v)"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="min_speech_duration_ms">
              <el-input-number
                :model-value="settingsStore.get('min_speech_duration_ms', 250)"
                :min="0"
                controls-position="right"
                @change="(v: number) => saveField('min_speech_duration_ms', v)"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="max_speech_duration_s">
              <el-input-number
                :model-value="settingsStore.get('max_speech_duration_s', 30)"
                :min="1"
                controls-position="right"
                @change="(v: number) => saveField('max_speech_duration_s', v)"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="min_silence_duration_ms">
              <el-input-number
                :model-value="settingsStore.get('min_silence_duration_ms', 500)"
                :min="0"
                controls-position="right"
                @change="(v: number) => saveField('min_silence_duration_ms', v)"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-tab-pane>

    <!-- Tab 3: Translation -->
    <el-tab-pane label="翻译" name="translation">
      <el-form label-position="top" :model="settingsStore.data">
        <el-form-item label="llm_chunk_size">
          <el-input-number
            :model-value="settingsStore.get('llm_chunk_size', 50)"
            :min="1"
            controls-position="right"
            @change="(v: number) => saveField('llm_chunk_size', v)"
          />
        </el-form-item>
        <el-form-item label="aitrans_temperature">
          <el-input-number
            :model-value="settingsStore.get('aitrans_temperature', 0.8)"
            :min="0"
            :max="2"
            :step="0.1"
            controls-position="right"
            @change="(v: number) => saveField('aitrans_temperature', v)"
          />
        </el-form-item>
        <el-form-item label="aitrans_context">
          <el-checkbox
            :model-value="settingsStore.get('aitrans_context', false)"
            @change="(v: boolean) => saveField('aitrans_context', v)"
          />
        </el-form-item>
      </el-form>
    </el-tab-pane>

    <!-- Tab 4: TTS -->
    <el-tab-pane label="TTS" name="tts">
      <el-form label-position="top" :model="settingsStore.data">
        <el-form-item label="edgetts_max_concurrent_tasks">
          <el-input-number
            :model-value="settingsStore.get('edgetts_max_concurrent_tasks', 5)"
            :min="1"
            controls-position="right"
            @change="(v: number) => saveField('edgetts_max_concurrent_tasks', v)"
          />
        </el-form-item>
        <el-form-item label="edgetts_retry_nums">
          <el-input-number
            :model-value="settingsStore.get('edgetts_retry_nums', 3)"
            :min="0"
            controls-position="right"
            @change="(v: number) => saveField('edgetts_retry_nums', v)"
          />
        </el-form-item>
      </el-form>
    </el-tab-pane>

    <!-- Tab 5: Processing -->
    <el-tab-pane label="处理" name="processing">
      <el-form label-position="top" :model="settingsStore.data">
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="trans_thread">
              <el-input-number
                :model-value="settingsStore.get('trans_thread', 5)"
                :min="1"
                controls-position="right"
                @change="(v: number) => saveField('trans_thread', v)"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="aitrans_thread">
              <el-input-number
                :model-value="settingsStore.get('aitrans_thread', 5)"
                :min="1"
                controls-position="right"
                @change="(v: number) => saveField('aitrans_thread', v)"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="dubbing_thread">
              <el-input-number
                :model-value="settingsStore.get('dubbing_thread', 3)"
                :min="1"
                controls-position="right"
                @change="(v: number) => saveField('dubbing_thread', v)"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="countdown_sec">
          <el-input-number
            :model-value="settingsStore.get('countdown_sec', 30)"
            :min="0"
            controls-position="right"
            @change="(v: number) => saveField('countdown_sec', v)"
          />
        </el-form-item>
        <el-form-item label="背景音量">
          <el-slider
            :model-value="settingsStore.get('backaudio_volume', 0.5)"
            :min="0"
            :max="2"
            :step="0.1"
            show-input
            @change="(v: number) => saveField('backaudio_volume', v)"
          />
        </el-form-item>
        <el-form-item label="loop_backaudio">
          <el-checkbox
            :model-value="settingsStore.get('loop_backaudio', false)"
            @change="(v: boolean) => saveField('loop_backaudio', v)"
          />
        </el-form-item>
      </el-form>
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()
const activeTab = ref('general')

const presets = [
  'ultrafast',
  'superfast',
  'veryfast',
  'faster',
  'fast',
  'medium',
  'slow',
  'slower',
  'veryslow',
]

const cudaComTypes = ['default', 'float16', 'int8', 'int8_float16']

async function saveField(key: string, value: any) {
  try {
    await settingsStore.save({ [key]: value })
  } catch (e: any) {
    ElMessage.error(e?.message ?? 'Save failed')
  }
}
</script>
