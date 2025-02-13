<script setup>
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'

const appStore = useAppStore()
const { loading } = storeToRefs(appStore)
</script>

<template>
  <transition name="fade">
    <div v-if="loading" class="global-loading">
      <div class="loading-content">
        <el-icon class="loading-icon" :size="40">
          <loading />
        </el-icon>
        <div class="loading-text">加载中...</div>
      </div>
    </div>
  </transition>
</template>

<style scoped lang="scss">
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-content {
  text-align: center;
}

.loading-icon {
  color: #409eff;
  animation: rotate 1s linear infinite;
}

.loading-text {
  margin-top: 10px;
  color: #606266;
  font-size: 14px;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
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