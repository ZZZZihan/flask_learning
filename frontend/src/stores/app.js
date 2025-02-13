import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const loading = ref(false)
  const error = ref(null)

  function startLoading() {
    loading.value = true
  }

  function stopLoading() {
    loading.value = false
  }

  function setError(message) {
    error.value = message
  }

  function clearError() {
    error.value = null
  }

  return {
    loading,
    error,
    startLoading,
    stopLoading,
    setError,
    clearError
  }
}) 