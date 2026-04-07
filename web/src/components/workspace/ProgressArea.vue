<template>
  <div class="progress-area">
    <el-progress
      :percentage="progressPercentage"
      :status="progressStatus"
      :stroke-width="18"
      text-inside
    />

    <div class="action-buttons">
      <el-button type="primary" :disabled="isRunning" @click="emit('start')">
        开始
      </el-button>
      <el-button type="danger" :disabled="!isRunning" @click="emit('stop')">
        停止
      </el-button>
    </div>

    <div ref="logContainer" class="log-area">
      <div v-for="(log, idx) in taskStore.activeLogs" :key="idx" class="log-line">
        {{ typeof log === 'string' ? log : log.text || JSON.stringify(log) }}
      </div>
      <div v-if="!taskStore.activeLogs.length" class="log-empty">
        暂无日志
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useTaskStore } from '@/stores/task'

const taskStore = useTaskStore()

const emit = defineEmits<{
  start: []
  stop: []
}>()

const logContainer = ref<HTMLDivElement>()

const isRunning = computed(() => {
  return taskStore.activeTask?.status === 'running'
})

const progressPercentage = computed(() => {
  const task = taskStore.activeTask
  if (!task) return 0
  if (task.status === 'completed') return 100
  if (task.status === 'failed') return 100
  // Derive progress from logs if available
  const logs = taskStore.activeLogs
  if (!logs.length) return 0
  const last = logs[logs.length - 1]
  if (typeof last === 'object' && last.progress != null) {
    return Math.min(100, Math.max(0, Number(last.progress)))
  }
  return 0
})

const progressStatus = computed(() => {
  const task = taskStore.activeTask
  if (!task) return undefined
  if (task.status === 'completed') return 'success' as const
  if (task.status === 'failed') return 'exception' as const
  return undefined
})

// Auto-scroll to bottom when new logs arrive
watch(
  () => taskStore.activeLogs.length,
  async () => {
    await nextTick()
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  }
)
</script>

<style scoped>
.progress-area {
  margin-top: 16px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin: 12px 0;
}

.log-area {
  height: 200px;
  overflow-y: auto;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  padding: 8px;
  background: var(--el-fill-color-blank);
  font-family: monospace;
  font-size: 12px;
  line-height: 1.6;
}

.log-line {
  white-space: pre-wrap;
  word-break: break-all;
}

.log-empty {
  color: var(--el-text-color-placeholder);
  text-align: center;
  padding-top: 80px;
}
</style>
