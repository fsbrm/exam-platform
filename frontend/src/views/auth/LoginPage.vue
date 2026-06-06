<template>
  <div class="auth-page">
    <div class="auth-card card">
      <h2 class="auth-title">登录</h2>
      <p class="auth-subtitle">欢迎回到智备考，请登录您的账号</p>

      <!-- Error Alert -->
      <transition name="el-fade-in">
        <el-alert v-if="errorMsg" :title="errorMsg" :type="errorType" show-icon :closable="true" @close="errorMsg=''" style="margin-bottom:16px" />
      </transition>

      <!-- Success Alert -->
      <transition name="el-fade-in">
        <el-alert v-if="successMsg" :title="successMsg" type="success" show-icon :closable="true" @close="successMsg=''" style="margin-bottom:16px" />
      </transition>

      <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleLogin" @keyup.enter="handleLogin" :disabled="locked">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名（2-32位字母数字下划线）"
            :prefix-icon="User"
            size="large"
            clearable
            @input="form.username = form.username.replace(/\s/g,'').trim()"
            @focus="onFieldFocus('username')"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码（6-64位）"
            :prefix-icon="Lock"
            size="large"
            show-password
            clearable
            @keyup="checkCapsLock"
            @focus="onFieldFocus('password')"
          />
        </el-form-item>

        <!-- Caps Lock Warning -->
        <transition name="el-fade-in">
          <div v-if="capsLockOn" class="caps-warn">
            <el-icon><WarningFilled /></el-icon> 大写锁定已开启
          </div>
        </transition>

        <!-- Lockout Countdown -->
        <div v-if="locked" class="lockout-info">
          <el-icon><Timer /></el-icon>
          登录尝试次数过多，请 {{ lockCountdown }} 秒后再试
        </div>

        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" :disabled="locked" native-type="submit" style="width:100%">
            {{ locked ? `请等待 ${lockCountdown} 秒` : loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <p class="auth-footer">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
      <p class="auth-footer-sub">
        忘记密码？请联系管理员重置
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { User, Lock, WarningFilled, Timer } from '@element-plus/icons-vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')
const errorType = ref<'error' | 'warning' | 'info'>('error')
const capsLockOn = ref(false)
const locked = ref(false)
const lockCountdown = ref(0)
let lockTimer: any = null

const form = reactive({ username: '', password: '' })

const rules = {
  username: [
    { required: true, message: '用户名不能为空，请输入您的用户名', trigger: 'blur' },
    { min: 2, message: '用户名不能少于 2 个字符', trigger: 'blur' },
    { max: 32, message: '用户名不能超过 32 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_一-龥]+$/, message: '用户名只能包含字母、数字、下划线和中文', trigger: 'blur' },
    { validator: (_r: any, v: string, cb: any) => { if (v && v.trim() !== v) cb(new Error('用户名首尾不能有空格')); else cb() }, trigger: 'blur' }
  ],
  password: [
    { required: true, message: '密码不能为空，请输入您的密码', trigger: 'blur' },
    { min: 6, message: '密码不能少于 6 个字符', trigger: 'blur' },
    { max: 64, message: '密码不能超过 64 个字符', trigger: 'blur' },
    { pattern: /^\S+$/, message: '密码不能包含空格', trigger: 'blur' }
  ]
}

function onFieldFocus(field: string) {
  // Clear field-specific error when user starts typing
  if (errorMsg.value && errorMsg.value.includes(field === 'username' ? '用户' : '密码')) {
    errorMsg.value = ''
  }
}

function checkCapsLock(e: KeyboardEvent) {
  capsLockOn.value = e.getModifierState?.('CapsLock') || false
}

function lockout(seconds: number) {
  locked.value = true
  lockCountdown.value = seconds
  clearInterval(lockTimer)
  lockTimer = setInterval(() => {
    lockCountdown.value--
    if (lockCountdown.value <= 0) {
      clearInterval(lockTimer)
      locked.value = false
      lockCountdown.value = 0
      errorMsg.value = ''
    }
  }, 1000)
}

onUnmounted(() => clearInterval(lockTimer))

async function handleLogin() {
  errorMsg.value = ''
  successMsg.value = ''
  errorType.value = 'error'

  // Pre-validation
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) {
    errorMsg.value = '请检查并修正表单中的输入错误后重新提交'
    errorType.value = 'warning'
    return
  }

  loading.value = true
  try {
    const res: any = await api.post('/auth/login', form, { timeout: 15000 })
    if (res.code === 200) {
      userStore.setToken(res.data.token)
      userStore.setUser(res.data)
      localStorage.setItem('user', JSON.stringify(res.data))
      const nickname = res.data?.nickname || res.data?.username || '用户'
      successMsg.value = `登录成功！欢迎回来，${nickname}`
      setTimeout(() => router.push('/'), 600)
    }
  } catch (e: any) {
    const status = e.response?.status
    const code = e.code
    const msg = e.response?.data?.message || ''

    // ── Network Errors ──
    if (code === 'ECONNABORTED' || code === 'ETIMEDOUT') {
      errorMsg.value = '请求超时，服务器响应过慢，请稍后重试或检查网络连接'
      errorType.value = 'warning'
    } else if (code === 'ERR_NETWORK' || code === 'ERR_CONNECTION_REFUSED') {
      errorMsg.value = '网络连接失败，请检查：\n1. 网络是否正常连接\n2. 服务器是否正在运行\n3. 是否存在防火墙或代理拦截'
      errorType.value = 'error'
    } else if (code === 'ERR_BAD_RESPONSE') {
      errorMsg.value = '服务器返回异常，可能正在维护中，请稍后再试'
      errorType.value = 'error'

    // ── HTTP Status Errors ──
    } else if (status === 400) {
      errorMsg.value = msg || '请求参数有误，请检查用户名和密码格式'
      errorType.value = 'warning'
    } else if (status === 401) {
      errorMsg.value = msg || '用户名或密码错误，请确认后重新输入'
      errorType.value = 'error'
      form.password = ''
    } else if (status === 403) {
      errorMsg.value = msg || '该账号已被管理员禁用，如有疑问请联系管理员'
      errorType.value = 'error'
    } else if (status === 404) {
      errorMsg.value = '服务接口不存在，请确认服务器版本是否正确'
      errorType.value = 'error'
    } else if (status === 429) {
      const retryAfter = e.response?.headers?.['retry-after']
      const sec = retryAfter ? parseInt(retryAfter) : 60
      errorMsg.value = `登录尝试过于频繁，为防止暴力破解已临时限制登录，请 ${sec} 秒后再试`
      errorType.value = 'warning'
      lockout(sec)
    } else if (status === 500) {
      errorMsg.value = msg || '服务器内部错误，可能正在维护或升级，请稍后重试'
      errorType.value = 'error'
    } else if (status === 502 || status === 503 || status === 504) {
      errorMsg.value = '服务器暂时不可用（网关/负载均衡异常），请稍后重试'
      errorType.value = 'error'
    } else if (status && status >= 500) {
      errorMsg.value = msg || `服务器错误（${status}），请稍后重试或联系管理员`
      errorType.value = 'error'

    // ── Other Errors ──
    } else if (e.message === 'Network Error') {
      errorMsg.value = '网络异常，请检查您的网络连接后重试'
      errorType.value = 'error'
    } else {
      errorMsg.value = msg || `登录失败（未知错误），请重试或联系管理员`
      errorType.value = 'error'
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
.auth-card { width: 420px; padding: 40px; }
.auth-title { font-size: 24px; font-weight: 700; text-align: center; margin-bottom: 8px; }
.auth-subtitle { text-align: center; color: var(--text-secondary); margin-bottom: 28px; font-size: 14px; }
.auth-footer { text-align: center; font-size: 14px; color: var(--text-secondary); margin-top: 16px; }
.auth-footer-sub { text-align: center; font-size: 12px; color: #9ca3af; margin-top: 8px; }

.caps-warn {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: #e6a23c; padding: 6px 12px;
  background: #fdf6ec; border-radius: 6px; margin-bottom: 12px;
}

.lockout-info {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; color: #f56c6c; padding: 10px 14px;
  background: #fef0f0; border-radius: 8px; margin-bottom: 12px;
  font-weight: 500;
}
</style>
