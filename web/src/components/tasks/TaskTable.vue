<template>
  <el-table :data="tasks" stripe style="width: 100%">
    <el-table-column prop="task_id" label="Task ID" width="220" show-overflow-tooltip />
    <el-table-column prop="task_type" label="类型" width="120" />
    <el-table-column label="文件" min-width="180" show-overflow-tooltip>
      <template #default="{ row }">
        {{ extractFilename(row.file) }}
      </template>
    </el-table-column>
    <el-table-column label="状态" width="120">
      <template #default="{ row }">
        <el-tag :type="statusTagType(row.status)" size="small">
          {{ row.status }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="创建时间" width="180">
      <template #default="{ row }">
        {{ formatTime(row.created_at) }}
      </template>
    </el-table-column>
    <el-table-column label="操作" width="200" fixed="right">
      <template #default="{ row }">
        <el-button size="small" @click="emit('view-logs', row.task_id)">
          查看日志
        </el-button>
        <el-button size="small" @click="emit('view-files', row.task_id)">
          查看文件
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts">
import type { TaskSummary } from '@/types/task'

defineProps<{
  tasks: TaskSummary[]
}>()

const emit = defineEmits<{
  'view-logs': [taskId: string]
  'view-files': [taskId: string]
}>()

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

function formatTime(ts: number | null): string {
  if (!ts) return '-'
  return new Date(ts * 1000).toLocaleString()
}
</script>
