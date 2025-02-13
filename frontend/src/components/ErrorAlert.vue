<script setup>
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'

const appStore = useAppStore()
const { error } = storeToRefs(appStore)
</script>

<template>
  <transition name="fade">
    <div v-if="error" class="error-alert">
      <el-alert
        :title="error"
        type="error"
        show-icon
        @close="appStore.clearError"
      />
    </div>
  </transition>
</template>

<style scoped lang="scss">
.error-alert {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  min-width: 300px;
  max-width: 80%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 