<template>
  <div class="alignment-section">
    <h4>对齐控制</h4>

    <el-form label-position="top" size="default">
      <el-form-item>
        <div class="checkbox-group">
          <el-checkbox v-model="paramsStore.data.voice_autorate">
            语音自动加速
          </el-checkbox>
          <el-checkbox v-model="paramsStore.data.video_autorate">
            视频自动加速
          </el-checkbox>
          <el-checkbox v-model="paramsStore.data.align_sub_audio">
            字幕音频对齐
          </el-checkbox>
        </div>
      </el-form-item>

      <el-form-item label="字幕类型">
        <el-select v-model="paramsStore.data.subtitle_type" class="full-width">
          <el-option label="不嵌入字幕" :value="0" />
          <el-option label="嵌入软字幕" :value="1" />
          <el-option label="嵌入硬字幕" :value="2" />
          <el-option label="仅字幕文件" :value="3" />
          <el-option label="视频+字幕文件" :value="4" />
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { useParamsStore } from '@/stores/params'

const paramsStore = useParamsStore()
</script>

<style scoped>
.alignment-section {
  margin-bottom: 16px;
}

.full-width {
  width: 100%;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
</style>
