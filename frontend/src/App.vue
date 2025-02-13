<script setup>
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'
import ErrorAlert from '@/components/ErrorAlert.vue'
import GlobalLoading from '@/components/GlobalLoading.vue'

const authStore = useAuthStore()

onMounted(async () => {
  if (authStore.token) {
    try {
      await authStore.getUserInfo()
    } catch (error) {
      console.error('Failed to get user info:', error)
    }
  }
})
</script>

<template>
  <el-container class="app-wrapper">
    <el-header>
      <nav class="nav-menu">
        <router-link to="/" class="logo">成就系统</router-link>
        <div class="nav-links">
          <template v-if="authStore.token">
            <router-link to="/achievements">成就列表</router-link>
            <router-link to="/achievements/new">新建成就</router-link>
            <el-dropdown>
              <span class="user-menu">
                {{ authStore.user?.username }}
                <el-icon><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="authStore.logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <router-link to="/login">登录</router-link>
            <router-link to="/register">注册</router-link>
          </template>
        </div>
      </nav>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
    <error-alert />
    <global-loading />
  </el-container>
</template>

<style scoped lang="scss">
.app-wrapper {
  min-height: 100vh;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  padding: 0;
}

.nav-menu {
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;

  a {
    color: #606266;
    text-decoration: none;

    &:hover {
      color: #409eff;
    }

    &.router-link-active {
      color: #409eff;
    }
  }
}

.user-menu {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.el-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

@media (max-width: 768px) {
  .nav-menu {
    padding: 0 10px;
  }

  .logo {
    font-size: 16px;
  }

  .nav-links {
    gap: 10px;
    font-size: 14px;
  }

  .el-main {
    padding: 10px;
  }
}
</style>
