import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useThemeStore = defineStore('useThemeStore', () => {
  const colors = ref<'white' | 'black'>(
    'black',
  )

  const applyBodyClass = (theme: 'white' | 'black') => {
    if (theme === 'black') {
      document.body.classList.add('theme-dark')
      document.body.classList.remove('theme-light')
    } else {
      document.body.classList.add('theme-light')
      document.body.classList.remove('theme-dark')
    }
  }

  const toggleTheme = () => {
    colors.value = colors.value === 'black' ? 'white' : 'black'
    localStorage.setItem('theme', colors.value)
    applyBodyClass(colors.value)
  }

  const switchPrimaryClass = computed(() => {
    return colors.value === 'black' ? 'text-white' : 'text-black'
  })

  const backgroundClass = computed(() => {
    return colors.value === 'black' ? 'bg-neutral-800' : 'bg-neutral-100'
  })

  // وقتی استور لود میشه، کلاس روی body ست بشه
  applyBodyClass(colors.value)

  // هر بار colors تغییر کرد، کلاس روی body آپدیت بشه
  watch(colors, (newTheme) => {
    applyBodyClass(newTheme)
  })

  return {
    colors,
    toggleTheme,
    switchPrimaryClass,
    backgroundClass,
  }
})
