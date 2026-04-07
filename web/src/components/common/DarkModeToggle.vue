<template>
  <el-switch
    v-model="appStore.darkMode"
    :active-action-icon="Moon"
    :inactive-action-icon="Sunny"
    @change="appStore.toggleDarkMode()"
    size="small"
  />
</template>

<script setup lang="ts">
import { Moon, Sunny } from '@element-plus/icons-vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
</script>
