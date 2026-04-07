<template>
  <div class="bg-audio-section">
    <h4>背景音频</h4>

    <el-form label-position="top" size="default">
      <el-form-item>
        <div class="checkbox-group">
          <el-checkbox v-model="paramsStore.data.is_separate">
            人声与背景分离
          </el-checkbox>
          <el-checkbox v-model="settingsStore.data.loop_backaudio">
            循环背景音
          </el-checkbox>
        </div>
      </el-form-item>

      <el-form-item label="背景音量">
        <el-slider
          v-model="settingsStore.data.backaudio_volume"
          :min="0"
          :max="2"
          :step="0.1"
          show-input
        />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { useParamsStore } from '@/stores/params'
import { useSettingsStore } from '@/stores/settings'

const paramsStore = useParamsStore()
const settingsStore = useSettingsStore()
</script>

<style scoped>
.bg-audio-section {
  margin-bottom: 16px;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
</style>
