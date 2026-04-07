<template>
  <div class="task-list-view">
    <div class="header">
      <h2>任务列表</h2>
      <el-button :icon="Refresh" :loading="loading" @click="loadTasks">
        刷新
      </el-button>
    </div>

    <TaskTable
      :tasks="taskStore.tasks"
      @view-logs="openLogs"
      @view-files="openFiles"
    />

    <TaskLogViewer
      v-model:visible="logViewerVisible"
      :task-id="selectedTaskId"
    />

    <TaskFileList
      v-model:visible="fileListVisible"
      :task-id="selectedTaskId"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import { useTaskStore } from '@/stores/task'
import TaskTable from '@/components/tasks/TaskTable.vue'
import TaskLogViewer from '@/components/tasks/TaskLogViewer.vue'
import TaskFileList from '@/components/tasks/TaskFileList.vue'

const taskStore = useTaskStore()
const loading = ref(false)
const logViewerVisible = ref(false)
const fileListVisible = ref(false)
const selectedTaskId = ref('')

async function loadTasks() {
  loading.value = true
  try {
    await taskStore.loadTasks()
  } finally {
    loading.value = false
  }
}

function openLogs(taskId: string) {
  selectedTaskId.value = taskId
  logViewerVisible.value = true
}

function openFiles(taskId: string) {
  selectedTaskId.value = taskId
  fileListVisible.value = true
}

onMounted(() => {
  loadTasks()
})
</script>

<style scoped>
.task-list-view {
  max-width: 1200px;
  margin: 0 auto;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.header h2 {
  margin: 0;
  color: var(--el-text-color-primary);
}
</style>
