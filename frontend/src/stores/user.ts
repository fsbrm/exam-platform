import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

interface UserInfo {
  userId: number
  username: string
  nickname: string
  avatar: string
  role: string
}

export const useUserStore = defineStore('user', () => {
  const savedUser = localStorage.getItem('user')
  const user = ref<UserInfo | null>(savedUser ? JSON.parse(savedUser) : null)
  const token = ref<string>(localStorage.getItem('token') || '')

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'ADMIN')

  function setUser(u: UserInfo) {
    user.value = u
    localStorage.setItem('user', JSON.stringify(u))
  }

  function setToken(t: string) {
    token.value = t
    localStorage.setItem('token', t)
  }

  function logout() {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function fetchProfile() {
    try {
      const res: any = await api.get('/auth/profile')
      if (res.code === 200) {
        user.value = res.data
        localStorage.setItem('user', JSON.stringify(res.data))
      }
    } catch (e) {
      logout()
    }
  }

  async function updateProfile(data: { nickname?: string; email?: string }) {
    const res: any = await api.put('/auth/profile', data)
    if (res.code === 200) {
      user.value = res.data
      localStorage.setItem('user', JSON.stringify(res.data))
    }
    return res
  }

  return { user, token, isLoggedIn, isAdmin, setUser, setToken, logout, fetchProfile, updateProfile }
})