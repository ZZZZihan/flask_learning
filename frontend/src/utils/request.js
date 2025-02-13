import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

const service = axios.create({
  baseURL: 'http://localhost:5001/api/v1',
  timeout: 5000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    const appStore = useAppStore()
    
    // 开始加载
    if (!config.hideLoading) {
      appStore.startLoading()
    }
    
    // 清除之前的错误
    appStore.clearError()
    
    if (authStore.token) {
      config.headers['Authorization'] = `Bearer ${authStore.token}`
    }
    return config
  },
  error => {
    const appStore = useAppStore()
    appStore.stopLoading()
    appStore.setError(error.message)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const appStore = useAppStore()
    appStore.stopLoading()
    const res = response.data
    return res
  },
  async error => {
    const authStore = useAuthStore()
    const appStore = useAppStore()
    
    appStore.stopLoading()
    
    if (error.response.status === 401) {
      // token过期，尝试刷新
      if (authStore.refreshToken) {
        try {
          await authStore.refreshToken()
          // 重试原请求
          const config = error.config
          config.headers['Authorization'] = `Bearer ${authStore.token}`
          return service(config)
        } catch (refreshError) {
          // 刷新token失败，需要重新登录
          authStore.logout()
          appStore.setError('登录已过期，请重新登录')
          ElMessage.error('登录已过期，请重新登录')
          return Promise.reject(refreshError)
        }
      } else {
        authStore.logout()
        appStore.setError('请先登录')
        ElMessage.error('请先登录')
      }
    } else {
      const errorMessage = error.response?.data?.message || '请求失败'
      appStore.setError(errorMessage)
      ElMessage.error(errorMessage)
    }
    return Promise.reject(error)
  }
)

export default service 