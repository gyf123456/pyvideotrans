<template>
  <div class="left-panel">
    <FileSelection @file-selected="onFileSelected" />

    <RecognitionSection
      v-if="showRecognition"
    />

    <TranslationSection
      v-if="showTranslation"
    />

    <TtsSection
      v-if="showTts"
    />

    <AlignmentSection
      v-if="showAlignment"
    />

    <BackgroundAudioSection
      v-if="showBackground"
    />

    <AdvancedSection
      v-if="showAdvanced"
    />

    <ProgressArea
      @start="emit('start')"
      @stop="emit('stop')"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import FileSelection from './FileSelection.vue'
import RecognitionSection from './RecognitionSection.vue'
import TranslationSection from './TranslationSection.vue'
import TtsSection from './TtsSection.vue'
import AlignmentSection from './AlignmentSection.vue'
import BackgroundAudioSection from './BackgroundAudioSection.vue'
import AdvancedSection from './AdvancedSection.vue'
import ProgressArea from './ProgressArea.vue'

const appStore = useAppStore()

const emit = defineEmits<{
  start: []
  stop: []
  'file-selected': [filepath: string]
}>()

const mode = computed(() => appStore.currentMode)

const showRecognition = computed(() =>
  ['biaozhun', 'tiqu', 'yuyinshibie'].includes(mode.value)
)

const showTranslation = computed(() =>
  ['biaozhun', 'tiqu', 'fanyi'].includes(mode.value)
)

const showTts = computed(() =>
  ['biaozhun', 'yuyinhecheng'].includes(mode.value)
)

const showAlignment = computed(() => mode.value === 'biaozhun')
const showBackground = computed(() => mode.value === 'biaozhun')
const showAdvanced = computed(() => mode.value === 'biaozhun')

function onFileSelected(filepath: string) {
  emit('file-selected', filepath)
}
</script>

<style scoped>
.left-panel {
  padding: 16px;
  height: 100%;
  overflow-y: auto;
}
</style>
