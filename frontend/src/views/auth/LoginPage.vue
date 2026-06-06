<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h2 class="auth-title">登录</h2>
      <p class="auth-subtitle">欢迎回到智备考</p>
      <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" native-type="submit" style="width:100%">
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <p class="auth-footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)

const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const res: any = await api.post('/auth/login', form)
    if (res.code === 200) {
      userStore.setToken(res.data.token)
      userStore.setUser(res.data)
      localStorage.setItem('user', JSON.stringify(res.data))
      ElMessage.success('登录成功')
      router.push('/')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex; justify-content: center; align-items: center;
  min-height: 100vh; padding-top: 60px; background: var(--bg-color);
}
.auth-card { width: 400px; padding: 40px; }
.auth-title { font-size: 24px; font-weight: 700; text-align: center; margin-bottom: 8px; }
.auth-subtitle { text-align: center; color: var(--text-secondary); margin-bottom: 32px; font-size: 14px; }
.auth-footer { text-align: center; font-size: 14px; color: var(--text-secondary); margin-top: 16px; }
</style>
