<template>
  <div class="advanced-section">
    <el-collapse v-model="activeNames">
      <el-collapse-item title="高级设置" name="advanced">
        <el-form label-position="top" size="default">
          <!-- Voice parameters -->
          <el-divider content-position="left">语音参数</el-divider>

          <el-row :gutter="12">
            <el-col :span="8">
              <el-form-item label="语速">
                <el-input v-model="paramsStore.data.voice_rate" placeholder="+0%" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="音量">
                <el-input v-model="paramsStore.data.volume" placeholder="+0%" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="音调">
                <el-input v-model="paramsStore.data.pitch" placeholder="+0Hz" />
              </el-form-item>
            </el-col>
          </el-row>

          <!-- Thread settings -->
          <el-divider content-position="left">线程设置</el-divider>

          <el-row :gutter="12">
            <el-col :span="8">
              <el-form-item label="翻译线程">
                <el-input-number v-model="paramsStore.data.trans_thread" :min="1" :max="20" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="AI翻译线程">
                <el-input-number v-model="paramsStore.data.aitrans_thread" :min="1" :max="20" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="配音线程">
                <el-input-number v-model="paramsStore.data.dubbing_thread" :min="1" :max="20" />
              </el-form-item>
            </el-col>
          </el-row>

          <!-- Speech detection parameters -->
          <el-divider content-position="left">语音检测参数</el-divider>

          <el-row :gutter="12">
            <el-col :span="12">
              <el-form-item label="阈值">
                <el-input-number
                  v-model="settingsStore.data.threshold"
                  :min="0"
                  :max="1"
                  :step="0.01"
                  :precision="2"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="最小语音时长(ms)">
                <el-input-number
                  v-model="settingsStore.data.min_speech_duration_ms"
                  :min="0"
                  :step="50"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="12">
            <el-col :span="12">
              <el-form-item label="最大语音时长(s)">
                <el-input-number
                  v-model="settingsStore.data.max_speech_duration_s"
                  :min="1"
                  :step="1"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="最小静音时长(ms)">
                <el-input-number
                  v-model="settingsStore.data.min_silence_duration_ms"
                  :min="0"
                  :step="50"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <!-- Subtitle length -->
          <el-divider content-position="left">字幕长度</el-divider>

          <el-row :gutter="12">
            <el-col :span="12">
              <el-form-item label="中日韩每行字数">
                <el-input-number v-model="settingsStore.data.cjk_len" :min="1" :max="200" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="其他语言每行字数">
                <el-input-number v-model="settingsStore.data.other_len" :min="1" :max="500" />
              </el-form-item>
            </el-col>
          </el-row>

          <!-- Proxy -->
          <el-divider content-position="left">网络</el-divider>

          <el-form-item label="代理">
            <el-input
              v-model="paramsStore.data.proxy"
              placeholder="http://127.0.0.1:7890"
            />
          </el-form-item>
        </el-form>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useParamsStore } from '@/stores/params'
import { useSettingsStore } from '@/stores/settings'

const paramsStore = useParamsStore()
const settingsStore = useSettingsStore()

const activeNames = ref<string[]>([])
</script>

<style scoped>
.advanced-section {
  margin-bottom: 16px;
}
</style>
