import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getParams, updateParams } from '@/api/config'

export const useParamsStore = defineStore('params', () => {
  const data = ref<Record<string, any>>({})
  const loaded = ref(false)

  async function load() {
    data.value = await getParams()
    loaded.value = true
  }

  async function save(partial: Record<string, any>) {
    Object.assign(data.value, partial)
    data.value = await updateParams(partial)
  }

  function get(key: string, defaultVal: any = '') {
    return data.value[key] ?? defaultVal
  }

  function set(key: string, value: any) {
    data.value[key] = value
  }

  return { data, loaded, load, save, get, set }
})
