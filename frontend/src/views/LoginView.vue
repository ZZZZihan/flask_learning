<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { usernameRules, passwordRules } from '@/utils/validation'

const router = useRouter()
const authStore = useAuthStore()

const loginForm = ref(null)
const formData = ref({
  username: '',
  password: ''
})

const handleSubmit = async () => {
  if (!loginForm.value) return
  
  await loginForm.value.validate(async (valid) => {
    if (valid) {
      try {
        await authStore.login(formData.value)
        router.push('/')
      } catch (error) {
        console.error('Login failed:', error)
      }
    }
  })
}
</script>

<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2 class="card-title">登录</h2>
      </template>
      
      <el-form
        ref="loginForm"
        :model="formData"
        :rules="{
          username: usernameRules,
          password: passwordRules
        }"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" style="width: 100%">
            登录
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <router-link to="/register">没有账号？立即注册</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.login-container {
  min-height: calc(100vh - 60px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.card-title {
  margin: 0;
  text-align: center;
  font-size: 24px;
  color: #303133;
}

.form-footer {
  margin-top: 20px;
  text-align: center;
  
  a {
    color: #409eff;
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
}

@media (max-width: 768px) {
  .login-card {
    max-width: 100%;
  }
  
  .card-title {
    font-size: 20px;
  }
}
</style> 