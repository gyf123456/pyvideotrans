<template>
  <el-dialog
    :model-value="visible"
    :title="providerConfig?.title ?? providerId"
    width="560px"
    destroy-on-close
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-form
      v-if="providerConfig"
      label-position="top"
      :model="formData"
      @submit.prevent
    >
      <el-form-item
        v-for="field in providerConfig.fields"
        :key="field.key"
        :label="field.label"
      >
        <!-- text -->
        <el-input
          v-if="field.type === 'text'"
          v-model="formData[field.key]"
          :placeholder="field.placeholder"
        />

        <!-- password -->
        <el-input
          v-else-if="field.type === 'password'"
          v-model="formData[field.key]"
          show-password
          :placeholder="field.placeholder"
        />

        <!-- select -->
        <el-select
          v-else-if="field.type === 'select'"
          v-model="formData[field.key]"
          filterable
          allow-create
          style="width: 100%"
        >
          <el-option
            v-for="opt in getSelectOptions(field)"
            :key="opt.value"
            :label="opt.label"
            :value="opt.value"
          />
        </el-select>

        <!-- textarea -->
        <el-input
          v-else-if="field.type === 'textarea'"
          v-model="formData[field.key]"
          type="textarea"
          :rows="3"
          :placeholder="field.placeholder"
        />

        <!-- models_editor -->
        <el-input
          v-else-if="field.type === 'models_editor'"
          v-model="formData[field.key]"
          type="textarea"
          :rows="4"
          :placeholder="field.placeholder ?? 'One model per line, or comma-separated'"
        />

        <!-- number -->
        <el-input-number
          v-else-if="field.type === 'number'"
          v-model="formData[field.key]"
          :min="field.min"
          :max="field.max"
          :step="field.step ?? 1"
          controls-position="right"
        />

        <!-- slider -->
        <el-slider
          v-else-if="field.type === 'slider'"
          v-model="formData[field.key]"
          :min="field.min ?? 0"
          :max="field.max ?? 100"
          :step="field.step ?? 1"
          show-input
        />

        <!-- checkbox -->
        <el-checkbox
          v-else-if="field.type === 'checkbox'"
          v-model="formData[field.key]"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="$emit('update:visible', false)">
        取消
      </el-button>
      <el-button type="primary" :loading="saving" @click="handleSave">
        保存
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { PROVIDER_CONFIGS } from '@/data/providerFields'
import type { ProviderFieldDef } from '@/data/providerFields'
import { useParamsStore } from '@/stores/params'
import { useSettingsStore } from '@/stores/settings'

const props = defineProps<{
  providerId: string
  visible: boolean
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  saved: []
}>()

const paramsStore = useParamsStore()
const settingsStore = useSettingsStore()
const saving = ref(false)
const formData = ref<Record<string, any>>({})

const providerConfig = computed(() => PROVIDER_CONFIGS[props.providerId])

watch(
  () => props.visible,
  (val) => {
    if (val && providerConfig.value) {
      const data: Record<string, any> = {}
      for (const field of providerConfig.value.fields) {
        data[field.key] = paramsStore.get(field.key, field.type === 'checkbox' ? false : '')
      }
      formData.value = data
    }
  },
)

function getSelectOptions(field: ProviderFieldDef): { label: string; value: any }[] {
  if (field.options) return field.options
  if (field.settingsKey) {
    const raw = settingsStore.get(field.settingsKey, '')
    if (!raw) return []
    return String(raw)
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
      .map((s) => ({ label: s, value: s }))
  }
  return []
}

async function handleSave() {
  saving.value = true
  try {
    await paramsStore.save(formData.value)
    ElMessage.success('保存成功')
    emit('saved')
    emit('update:visible', false)
  } catch (e: any) {
    ElMessage.error(e?.message ?? '保存失败')
  } finally {
    saving.value = false
  }
}
</script>
