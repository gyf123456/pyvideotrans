<template>
  <div class="translation-section">
    <h4>翻译</h4>

    <el-form label-position="top" size="default">
      <el-form-item label="翻译引擎">
        <el-select v-model="paramsStore.data.translate_type" class="full-width">
          <el-option
            v-for="item in providersStore.translationList"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="源语言">
        <el-select v-model="paramsStore.data.source_language" class="full-width" filterable>
          <el-option label="自动检测" value="auto" />
          <el-option
            v-for="lang in providersStore.languages"
            :key="lang.code"
            :label="lang.name"
            :value="lang.code"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="目标语言">
        <el-select v-model="paramsStore.data.target_language" class="full-width" filterable>
          <el-option
            v-for="lang in providersStore.languages"
            :key="lang.code"
            :label="lang.name"
            :value="lang.code"
          />
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { useParamsStore } from '@/stores/params'
import { useProvidersStore } from '@/stores/providers'

const paramsStore = useParamsStore()
const providersStore = useProvidersStore()
</script>

<style scoped>
.translation-section {
  margin-bottom: 16px;
}

.full-width {
  width: 100%;
}
</style>
