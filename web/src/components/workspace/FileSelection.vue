<template>
  <div class="file-selection">
    <el-upload
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleFileChange"
      drag
      multiple
    >
      <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
      <div class="el-upload__text">
        将文件拖到此处
        <em>或点击上传</em>
      </div>
    </el-upload>

    <div v-if="uploading" class="upload-status">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>上传中...</span>
    </div>

    <ul v-if="fileList.length" class="file-list">
      <li v-for="(f, idx) in fileList" :key="idx" class="file-item">
        <el-icon><Document /></el-icon>
        <span class="file-name">{{ f.name }}</span>
        <el-icon class="remove-btn" @click="removeFile(idx)"><Close /></el-icon>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled, Document, Close, Loading } from '@element-plus/icons-vue'
import { uploadFile as apiUploadFile } from '@/api/upload'
import { ElMessage } from 'element-plus'
import type { UploadFile } from 'element-plus'

interface FileEntry {
  name: string
  filepath: string
}

const emit = defineEmits<{
  'file-selected': [filepath: string]
}>()

const fileList = ref<FileEntry[]>([])
const uploading = ref(false)

async function handleFileChange(file: UploadFile) {
  if (!file.raw) return
  uploading.value = true
  try {
    const result = await apiUploadFile(file.raw)
    const entry: FileEntry = { name: file.name, filepath: result.filepath }
    fileList.value.push(entry)
    emit('file-selected', result.filepath)
  } catch (e: any) {
    ElMessage.error(e.message || 'Upload failed')
  } finally {
    uploading.value = false
  }
}

function removeFile(index: number) {
  fileList.value.splice(index, 1)
}
</script>

<style scoped>
.file-selection {
  margin-bottom: 16px;
}

.upload-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  color: var(--el-color-primary);
}

.file-list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-radius: 4px;
  background: var(--el-fill-color-light);
  margin-bottom: 4px;
}

.file-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-btn {
  cursor: pointer;
  color: var(--el-color-danger);
}
</style>
