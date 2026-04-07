<template>
  <div class="settings-view">
    <h2>设置</h2>

    <GeneralSettings />

    <div class="provider-section" v-for="group in providerGroups" :key="group.category">
      <h3>{{ group.title }}</h3>
      <el-row :gutter="12">
        <el-col
          v-for="provider in group.providers"
          :key="provider.id"
          :xs="12"
          :sm="8"
          :md="6"
          :lg="4"
        >
          <el-card
            shadow="hover"
            class="provider-card"
            @click="openProvider(provider.id)"
          >
            <span class="provider-title">{{ provider.title }}</span>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <ProviderConfigDialog
      v-model:visible="dialogVisible"
      :provider-id="activeProviderId"
      @saved="onProviderSaved"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { PROVIDER_CONFIGS } from '@/data/providerFields'
import GeneralSettings from '@/components/settings/GeneralSettings.vue'
import ProviderConfigDialog from '@/components/settings/ProviderConfigDialog.vue'

const dialogVisible = ref(false)
const activeProviderId = ref('')

const providerGroups = computed(() => {
  const configs = Object.values(PROVIDER_CONFIGS)
  return [
    {
      category: 'translation',
      title: '翻译服务商',
      providers: configs.filter((c) => c.category === 'translation'),
    },
    {
      category: 'tts',
      title: '配音服务商',
      providers: configs.filter((c) => c.category === 'tts'),
    },
    {
      category: 'recognition',
      title: '语音识别服务商',
      providers: configs.filter((c) => c.category === 'recognition'),
    },
  ]
})

function openProvider(id: string) {
  activeProviderId.value = id
  dialogVisible.value = true
}

function onProviderSaved() {
  // Provider config saved successfully - dialog closes automatically
}
</script>

<style scoped>
.settings-view {
  max-width: 1200px;
  margin: 0 auto;
}
.settings-view h2 {
  margin: 0 0 20px 0;
  color: var(--el-text-color-primary);
}
.provider-section {
  margin-top: 28px;
}
.provider-section h3 {
  margin: 0 0 12px 0;
  color: var(--el-text-color-regular);
  font-size: 16px;
}
.provider-card {
  margin-bottom: 12px;
  cursor: pointer;
  text-align: center;
}
.provider-card :deep(.el-card__body) {
  padding: 14px 8px;
}
.provider-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}
</style>
