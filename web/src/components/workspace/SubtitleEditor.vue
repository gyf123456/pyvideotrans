<template>
  <div class="subtitle-editor">
    <el-row :gutter="16">
      <el-col :span="12">
        <div class="subtitle-panel">
          <h4>原始字幕</h4>
          <el-input
            type="textarea"
            :model-value="sourceText"
            readonly
            :rows="20"
            resize="none"
          />
        </div>
      </el-col>
      <el-col :span="12">
        <div class="subtitle-panel">
          <h4>目标字幕</h4>
          <el-input
            type="textarea"
            :model-value="targetText"
            readonly
            :rows="20"
            resize="none"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  sourceText: string
  targetText: string
}>()
</script>

<style scoped>
.subtitle-editor {
  height: 100%;
}

.subtitle-panel h4 {
  margin: 0 0 8px;
}

.subtitle-panel :deep(.el-textarea__inner) {
  font-family: monospace;
  font-size: 13px;
  line-height: 1.6;
}
</style>
