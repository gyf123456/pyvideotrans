<template>
  <el-container class="main-layout">
    <AppHeader />
    <el-main class="main-content">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import AppHeader from '@/components/common/AppHeader.vue'
import { useSettingsStore } from '@/stores/settings'
import { useParamsStore } from '@/stores/params'
import { useProvidersStore } from '@/stores/providers'

const settingsStore = useSettingsStore()
const paramsStore = useParamsStore()
const providersStore = useProvidersStore()

onMounted(async () => {
  await Promise.all([
    settingsStore.load(),
    paramsStore.load(),
    providersStore.loadAll(),
  ])
})
</script>

<style scoped>
.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  overflow: auto;
  padding: 20px;
  background: var(--el-bg-color-page);
}
</style>
