<template>
  <el-drawer
    :model-value="visible"
    title="文件"
    size="40%"
    destroy-on-close
    @update:model-value="$emit('update:visible', $event)"
    @open="handleOpen"
  >
    <el-table :data="files" stripe style="width: 100%" v-loading="loading">
      <el-table-column label="文件名" min-width="200" show-overflow-tooltip>
        <template #default="{ row }">
          {{ row.name }}
        </template>
      </el-table-column>
      <el-table-column label="文件大小" width="120">
        <template #default="{ row }">
          {{ formatSize(row.size) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button size="small" type="primary" link @click="downloadFile(row.path)">
            下载
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-empty v-if="!loading && files.length === 0" description="暂无文件" />
  </el-drawer>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { listFiles, getDownloadUrl } from '@/api/files'
import type { FileItem } from '@/types/config'

const props = defineProps<{
  visible: boolean
  taskId: string
}>()

defineEmits<{
  'update:visible': [value: boolean]
}>()

const files = ref<FileItem[]>([])
const loading = ref(false)

async function handleOpen() {
  if (!props.taskId) return
  loading.value = true
  try {
    files.value = await listFiles(props.taskId)
  } catch {
    files.value = []
  } finally {
    loading.value = false
  }
}

function formatSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + units[i]
}

function downloadFile(path: string) {
  window.open(getDownloadUrl(path), '_blank')
}
</script>
