<template>
  <div class="right-panel">
    <ModeToolbar />
    <SubtitleEditor
      :source-text="sourceText"
      :target-text="targetText"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ModeToolbar from './ModeToolbar.vue'
import SubtitleEditor from './SubtitleEditor.vue'

const sourceText = ref('')
const targetText = ref('')
</script>

<style scoped>
.right-panel {
  padding: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
</style>
