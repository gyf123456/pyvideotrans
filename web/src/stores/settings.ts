import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getSettings, updateSettings } from '@/api/config'

export const useSettingsStore = defineStore('settings', () => {
  const data = ref<Record<string, any>>({})
  const loaded = ref(false)

  async function load() {
    data.value = await getSettings()
    loaded.value = true
  }

  async function save(partial: Record<string, any>) {
    Object.assign(data.value, partial)
    data.value = await updateSettings(partial)
  }

  function get(key: string, defaultVal: any = '') {
    return data.value[key] ?? defaultVal
  }

  return { data, loaded, load, save, get }
})
