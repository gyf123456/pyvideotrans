import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProviders } from '@/api/providers'
import { getLanguages } from '@/api/languages'
import type { ProviderItem, LanguageItem } from '@/types/provider'

export const useProvidersStore = defineStore('providers', () => {
  const recognitionList = ref<ProviderItem[]>([])
  const translationList = ref<ProviderItem[]>([])
  const ttsList = ref<ProviderItem[]>([])
  const languages = ref<LanguageItem[]>([])
  const loaded = ref(false)

  async function loadAll() {
    const [r, t, s, l] = await Promise.all([
      getProviders('recognition'),
      getProviders('translation'),
      getProviders('tts'),
      getLanguages(),
    ])
    recognitionList.value = r
    translationList.value = t
    ttsList.value = s
    languages.value = l
    loaded.value = true
  }

  return { recognitionList, translationList, ttsList, languages, loaded, loadAll }
})
