<template>
  <div class="workspace-view">
    <el-row :gutter="20" class="workspace-row">
      <el-col :span="13">
        <div class="panel">
          <LeftPanel
            @start="handleStart"
            @stop="handleStop"
            @file-selected="onFileSelected"
          />
        </div>
      </el-col>
      <el-col :span="11">
        <div class="panel">
          <RightPanel />
          <div class="task-info" v-if="currentTaskId">
            <el-descriptions :column="2" border size="small">
              <el-descriptions-item label="Task ID">{{ currentTaskId }}</el-descriptions-item>
              <el-descriptions-item label="Status">
                <el-tag :type="statusTag" size="small">{{ currentStatus }}</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </div>
          <div ref="logAreaRef" class="log-area">
            <pre class="log-text">{{ logOutput }}</pre>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadFile } from '@/api/upload'
import { createTask } from '@/api/tasks'
import { useParamsStore } from '@/stores/params'
import { useAppStore } from '@/stores/app'
import { useTaskStore } from '@/stores/task'
import { useTaskWebSocket } from '@/composables/useTaskWebSocket'
import LeftPanel from '@/components/workspace/LeftPanel.vue'
import RightPanel from '@/components/workspace/RightPanel.vue'

const paramsStore = useParamsStore()
const appStore = useAppStore()
const taskStore = useTaskStore()
const { connect, disconnect } = useTaskWebSocket()

const uploadedFilePath = ref('')
const currentTaskId = ref('')
const currentStatus = ref('')
const logAreaRef = ref<HTMLElement | null>(null)

const statusTag = computed(() => {
  const map: Record<string, string> = {
    pending: 'info', running: 'warning', completed: 'success', failed: 'danger',
  }
  return map[currentStatus.value] || 'info'
})

const logOutput = computed(() =>
  taskStore.activeLogs
    .map((log) => (typeof log === 'string' ? log : log.text ?? JSON.stringify(log)))
    .join('\n')
)

watch(logOutput, async () => {
  await nextTick()
  if (logAreaRef.value) {
    logAreaRef.value.scrollTop = logAreaRef.value.scrollHeight
  }
})

watch(() => taskStore.activeTask?.status, (status) => {
  if (status) currentStatus.value = status
})

function onFileSelected(filepath: string) {
  uploadedFilePath.value = filepath
}

// Map app mode to task type
function getTaskType(): 'stt' | 'tts' | 'sts' | 'vtv' {
  const modeMap: Record<string, 'stt' | 'tts' | 'sts' | 'vtv'> = {
    biaozhun: 'vtv',
    tiqu: 'stt',
    yuyinshibie: 'stt',
    fanyi: 'sts',
    yuyinhecheng: 'tts',
  }
  return modeMap[appStore.currentMode] || 'vtv'
}

async function handleStart() {
  if (!uploadedFilePath.value) {
    ElMessage.warning('Please upload a file first')
    return
  }

  taskStore.clearLogs()
  currentStatus.value = 'pending'

  try {
    const taskType = getTaskType()
    const p = paramsStore.data
    const req = {
      task: taskType,
      name: uploadedFilePath.value,
      recogn_type: p.recogn_type ?? 0,
      detect_language: p.source_language ?? 'auto',
      model_name: p.model_name ?? 'tiny',
      is_cuda: p.is_cuda ?? false,
      remove_noise: p.remove_noise ?? false,
      enable_diariz: p.enable_diariz ?? false,
      nums_diariz: p.nums_diariz ?? -1,
      rephrase: p.rephrase ?? 0,
      fix_punc: p.fix_punc ?? false,
      tts_type: p.tts_type ?? 0,
      voice_role: p.voice_role ?? 'No',
      voice_rate: `+${p.voice_rate ?? 0}%`,
      volume: `+${p.volume ?? 0}%`,
      pitch: `+${p.pitch ?? 0}Hz`,
      voice_autorate: p.voice_autorate ?? false,
      video_autorate: p.video_autorate ?? false,
      align_sub_audio: p.align_sub_audio ?? false,
      target_language_code: p.target_language ?? undefined,
      translate_type: p.translate_type ?? 0,
      source_language_code: p.source_language ?? undefined,
      is_separate: p.is_separate ?? false,
      recogn2pass: p.recogn2pass ?? false,
      subtitle_type: p.subtitle_type ?? 1,
      clear_cache: true,
    }

    const result = await createTask(req)
    currentTaskId.value = result.task_id
    currentStatus.value = 'pending'
    connect(result.task_id)
    ElMessage.success('Task created')
  } catch (e: any) {
    ElMessage.error(e?.message ?? 'Failed to create task')
    currentStatus.value = 'failed'
  }
}

function handleStop() {
  disconnect()
  currentStatus.value = 'stopped'
  ElMessage.info('Task disconnected')
}
</script>

<style scoped>
.workspace-view {
  height: 100%;
}
.workspace-row {
  height: 100%;
}
.panel {
  background: var(--el-bg-color);
  border-radius: 8px;
  padding: 16px;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.task-info {
  margin: 12px 0;
  flex-shrink: 0;
}
.log-area {
  flex: 1;
  overflow-y: auto;
  background: var(--el-fill-color-darker, #1a1a2e);
  border-radius: 4px;
  padding: 12px;
  min-height: 200px;
}
.log-text {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.6;
  color: var(--el-text-color-primary);
}
</style>
