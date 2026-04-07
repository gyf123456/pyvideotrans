<template>
  <div class="recognition-section">
    <h4>语音识别</h4>

    <el-form label-position="top" size="default">
      <el-form-item label="识别引擎">
        <el-select v-model="paramsStore.data.recogn_type" class="full-width">
          <el-option
            v-for="item in providersStore.recognitionList"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="模型">
        <el-select v-model="paramsStore.data.model_name" class="full-width" filterable allow-create>
          <el-option
            v-for="name in modelOptions"
            :key="name"
            :label="name"
            :value="name"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="重新断句">
        <el-select v-model="paramsStore.data.rephrase" class="full-width">
          <el-option label="默认" :value="0" />
          <el-option label="LLM断句" :value="1" />
        </el-select>
      </el-form-item>

      <el-form-item>
        <div class="checkbox-group">
          <el-checkbox v-model="paramsStore.data.is_cuda">CUDA加速</el-checkbox>
          <el-checkbox v-model="paramsStore.data.remove_noise">降噪</el-checkbox>
          <el-checkbox v-model="paramsStore.data.fix_punc">标点修复</el-checkbox>
          <el-checkbox v-model="paramsStore.data.enable_diariz">说话人分离</el-checkbox>
        </div>
      </el-form-item>

      <el-form-item v-if="paramsStore.data.enable_diariz" label="说话人数量">
        <el-input-number
          v-model="paramsStore.data.nums_diariz"
          :min="1"
          :max="20"
          :step="1"
        />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useParamsStore } from '@/stores/params'
import { useProvidersStore } from '@/stores/providers'
import { useSettingsStore } from '@/stores/settings'

const paramsStore = useParamsStore()
const providersStore = useProvidersStore()
const settingsStore = useSettingsStore()

const modelOptions = computed(() => {
  const raw = settingsStore.get('model_list', '')
  if (!raw) return []
  return raw.split(',').map((s: string) => s.trim()).filter(Boolean)
})
</script>

<style scoped>
.recognition-section {
  margin-bottom: 16px;
}

.full-width {
  width: 100%;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
</style>
