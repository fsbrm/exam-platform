import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // Don't redirect on login/register requests - let the page handle it
      const isAuthRequest = error.config?.url?.includes('/auth/login') || error.config?.url?.includes('/auth/register')
      if (!isAuthRequest) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
      }
      ElMessage.error(error.response?.data?.message || (isAuthRequest ? '登录失败' : '登录已过期，请重新登录'))
    } else if (error.response?.status === 403) {
      ElMessage.error(error.response?.data?.message || '权限不足')
    } else {
      ElMessage.error(error.response?.data?.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default api