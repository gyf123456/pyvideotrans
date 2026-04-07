<template>
  <el-drawer
    :model-value="visible"
    title="日志"
    size="50%"
    destroy-on-close
    @update:model-value="$emit('update:visible', $event)"
    @open="handleOpen"
    @close="handleClose"
  >
    <div v-if="taskDetail" class="task-info">
      <el-descriptions :column="3" border size="small">
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(taskDetail.status)" size="small">
            {{ taskDetail.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="类型">
          {{ taskDetail.task_type }}
        </el-descriptions-item>
        <el-descriptions-item label="文件">
          {{ extractFilename(taskDetail.file) }}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <div v-if="taskDetail?.error" class="task-error">
      <el-alert :title="taskDetail.error" type="error" show-icon :closable="false" />
    </div>

    <div ref="logContainerRef" class="log-container">
      <pre class="log-content">{{ logText }}</pre>
    </div>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { getTask } from '@/api/tasks'
import { useTaskWebSocket } from '@/composables/useTaskWebSocket'
import { useTaskStore } from '@/stores/task'
import type { TaskStatusResponse } from '@/types/task'

const props = defineProps<{
  visible: boolean
  taskId: string
}>()

defineEmits<{
  'update:visible': [value: boolean]
}>()

const taskStore = useTaskStore()
const { connect, disconnect } = useTaskWebSocket()

const taskDetail = ref<TaskStatusResponse | null>(null)
const logContainerRef = ref<HTMLElement | null>(null)

const logText = computed(() => {
  const lines: string[] = []
  // Include initial logs from task detail
  if (taskDetail.value?.logs) {
    for (const log of taskDetail.value.logs) {
      lines.push(typeof log === 'string' ? log : log.text ?? JSON.stringify(log))
    }
  }
  // Include real-time logs from store
  for (const log of taskStore.activeLogs) {
    lines.push(typeof log === 'string' ? log : log.text ?? JSON.stringify(log))
  }
  return lines.join('\n')
})

watch(logText, async () => {
  await nextTick()
  scrollToBottom()
})

function scrollToBottom() {
  if (logContainerRef.value) {
    logContainerRef.value.scrollTop = logContainerRef.value.scrollHeight
  }
}

async function handleOpen() {
  taskStore.clearLogs()
  taskDetail.value = null
  if (!props.taskId) return
  try {
    taskDetail.value = await getTask(props.taskId)
    // Connect WebSocket for real-time updates if task is still active
    if (
      taskDetail.value.status === 'pending' ||
      taskDetail.value.status === 'running'
    ) {
      connect(props.taskId)
    }
  } catch {
    // ignore
  }
}

function handleClose() {
  disconnect()
  taskStore.clearLogs()
}

function statusTagType(status: string): '' | 'info' | 'warning' | 'success' | 'danger' {
  switch (status) {
    case 'pending':
      return 'info'
    case 'running':
      return 'warning'
    case 'completed':
      return 'success'
    case 'failed':
      return 'danger'
    default:
      return 'info'
  }
}

function extractFilename(filepath: string): string {
  if (!filepath) return ''
  return filepath.replace(/\\/g, '/').split('/').pop() ?? filepath
}
</script>

<style scoped>
.task-info {
  margin-bottom: 16px;
}
.task-error {
  margin-bottom: 16px;
}
.log-container {
  flex: 1;
  overflow-y: auto;
  background: var(--el-fill-color-darker, #1e1e1e);
  border-radius: 4px;
  padding: 12px;
  max-height: calc(100vh - 260px);
}
.log-content {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.6;
  color: var(--el-text-color-primary);
}
</style>
