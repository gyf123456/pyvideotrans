<template>
  <div class="mode-toolbar">
    <el-radio-group v-model="appStore.currentMode" size="default">
      <el-radio-button value="biaozhun">
        标准模式
      </el-radio-button>
      <el-radio-button value="tiqu">
        提取字幕
      </el-radio-button>
      <el-radio-button value="yuyinshibie">
        语音识别
      </el-radio-button>
      <el-radio-button value="fanyi">
        翻译
      </el-radio-button>
      <el-radio-button value="yuyinhecheng">
        语音合成
      </el-radio-button>
    </el-radio-group>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
</script>

<style scoped>
.mode-toolbar {
  margin-bottom: 16px;
}
</style>
