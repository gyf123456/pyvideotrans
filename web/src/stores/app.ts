import { defineStore } from 'pinia'
import { ref } from 'vue'

export type AppMode = 'biaozhun' | 'tiqu' | 'yuyinshibie' | 'fanyi' | 'yuyinhecheng'

export const useAppStore = defineStore('app', () => {
  const locale = ref<string>('en')
  const darkMode = ref(false)
  const currentMode = ref<AppMode>('biaozhun')

  function setLocale(lang: string) {
    locale.value = lang
    localStorage.setItem('locale', lang)
  }

  function toggleDarkMode() {
    darkMode.value = !darkMode.value
    localStorage.setItem('darkMode', String(darkMode.value))
    document.documentElement.classList.toggle('dark', darkMode.value)
  }

  function setMode(mode: AppMode) {
    currentMode.value = mode
  }

  function init() {
    const savedLocale = localStorage.getItem('locale')
    if (savedLocale) locale.value = savedLocale
    const savedDark = localStorage.getItem('darkMode')
    if (savedDark === 'true') {
      darkMode.value = true
      document.documentElement.classList.add('dark')
    }
  }

  return { locale, darkMode, currentMode, setLocale, toggleDarkMode, setMode, init }
})
