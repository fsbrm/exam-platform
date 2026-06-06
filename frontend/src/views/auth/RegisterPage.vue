<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h2 class="auth-title">注册</h2>
      <p class="auth-subtitle">需要邀请码才能注册，请联系管理员获取</p>
      <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleRegister">
        <el-form-item prop="inviteCode">
          <el-input v-model="form.inviteCode" placeholder="邀请码（必填）" size="large" />
        </el-form-item>
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码（至少6位）" size="large" show-password />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="邮箱（选填）" size="large" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" native-type="submit" style="width:100%">
            注册
          </el-button>
        </el-form-item>
      </el-form>
      <p class="auth-footer">
        已有账号？<router-link to="/login">立即登录</router-link>
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

const form = reactive({ username: '', password: '', email: '', nickname: '', inviteCode: '' })
const rules = {
  inviteCode: [
    { required: true, message: '请输入邀请码', trigger: 'blur' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度3-50位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ]
}

async function handleRegister() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const res: any = await api.post('/auth/register', {
      username: form.username,
      password: form.password,
      email: form.email,
      nickname: form.username,
      inviteCode: form.inviteCode
    })
    if (res.code === 200) {
      userStore.setToken(res.data.token)
      userStore.setUser(res.data)
      ElMessage.success('注册成功！')
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