import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, register, getInfo, refreshToken } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref('')
  const refreshTokenValue = ref('')
  const user = ref(null)

  async function loginAction(loginData) {
    const res = await login(loginData)
    token.value = res.access_token
    refreshTokenValue.value = res.refresh_token
    await getUserInfo()
  }

  async function registerAction(registerData) {
    await register(registerData)
  }

  async function getUserInfo() {
    const res = await getInfo()
    user.value = res
  }

  async function refreshTokenAction() {
    const res = await refreshToken()
    token.value = res.access_token
  }

  function logout() {
    token.value = ''
    refreshTokenValue.value = ''
    user.value = null
  }

  return {
    token,
    refreshToken: refreshTokenValue,
    user,
    loginAction,
    registerAction,
    getUserInfo,
    refreshTokenAction,
    logout
  }
}) 