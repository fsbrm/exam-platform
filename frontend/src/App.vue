<template>
  <div id="app">
    <!-- Global Navigation -->
    <header class="app-header">
      <div class="header-inner">
        <!-- Practice page header -->
        <template v-if="route.path.startsWith('/practice')">
          <button class="ph-back" @click="$router.back()"><span>&larr;</span> 返回真题总览</button>
          <span class="ph-title">刷题练习</span>
          <span class="ph-spacer"></span>
          <div class="ph-settings-wrap">
            <button class="ph-settings-btn" @click.stop="showSettings = !showSettings" title="刷题设置">
              <el-icon :size="18"><Setting /></el-icon>
            </button>
            <div class="ph-settings-drop" v-if="showSettings" @click.stop>
              <div class="psd-item">
                <span>做题反馈</span>
                <el-switch v-model="feedbackEnabled" size="small" @change="saveSetting" />
              </div>
              <div class="psd-item">
                <span>键盘快捷键</span>
                <el-switch v-model="keyboardEnabled" size="small" @change="saveSetting" />
              </div>
              <div class="psd-item">
                <span>连击计数</span>
                <el-switch v-model="comboEnabled" size="small" @change="saveSetting" />
              </div>
              <div class="psd-item">
                <span>自动提交</span>
                <el-switch v-model="autoSubmit" size="small" @change="saveSetting" />
              </div>
            </div>
          </div>
          <router-link to="/papers" class="ph-link">真题总览</router-link>
        </template>
        <!-- Normal navigation -->
        <template v-else>
        <router-link to="/" class="logo">
          <span class="logo-icon">🎓</span>
          <span class="logo-text">408真题</span>
        </router-link>
        <nav class="main-nav">
          <router-link to="/" class="nav-item" active-class="nav-active">
            <span class="nav-icon">📊</span>首页
          </router-link>
          <router-link to="/papers" class="nav-item" active-class="nav-active">
            <span class="nav-icon">📋</span>真题总览
          </router-link>
          <router-link to="/knowledge" class="nav-item" active-class="nav-active">
            <span class="nav-icon">🕸️</span>知识图谱
          </router-link>
          <router-link to="/practice" class="nav-item" active-class="nav-active">
            <span class="nav-icon">📝</span>刷题练习
          </router-link>
          <router-link to="/exam" class="nav-item" active-class="nav-active">
            <span class="nav-icon">⏱️</span>模拟考试
          </router-link>
          <router-link to="/wrong" class="nav-item" active-class="nav-active">
            <span class="nav-icon">📌</span>错题本
          </router-link>
          <router-link to="/analytics" class="nav-item" active-class="nav-active">
            <span class="nav-icon">📈</span>学习分析
          </router-link>
          <router-link to="/ai" class="nav-item" active-class="nav-active">
            <span class="nav-icon">🤖</span>AI助手
          </router-link>
          <router-link v-if="userStore.isAdmin" to="/admin" class="nav-item" active-class="nav-active">
            <span class="nav-icon">⚙️</span>管理后台
          </router-link>
        </nav>
                </template>
        <div class="user-area">
          <template v-if="userStore.isLoggedIn">
            <router-link to="/profile" class="user-btn">{{ userStore.user?.nickname || userStore.user?.username }}</router-link>
            <button class="logout-btn" @click="logout">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="login-btn">登录</router-link>
          </template>
        </div>
      </div>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter, useRoute } from 'vue-router'
import { Setting } from '@element-plus/icons-vue'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

// Practice settings
const showSettings = ref(false)
const feedbackEnabled = ref(localStorage.getItem('practice_feedback') === 'true')
const keyboardEnabled = ref(localStorage.getItem('practice_keyboard') === 'true')
const comboEnabled = ref(localStorage.getItem('practice_combo') === 'true')
const autoSubmit = ref(localStorage.getItem('practice_autosubmit') === 'true')
function saveSetting() {
  localStorage.setItem('practice_feedback', String(feedbackEnabled.value))
  localStorage.setItem('practice_keyboard', String(keyboardEnabled.value))
  localStorage.setItem('practice_combo', String(comboEnabled.value))
  localStorage.setItem('practice_autosubmit', String(autoSubmit.value))
}
// Auto-close settings on outside click or scroll
function closeSettings() { showSettings.value = false }
onMounted(() => {
  document.addEventListener('click', closeSettings)
  document.addEventListener('scroll', closeSettings, true)
})
onUnmounted(() => {
  document.removeEventListener('click', closeSettings)
  document.removeEventListener('scroll', closeSettings, true)
})

function logout() {
  userStore.logout()
  router.push('/')
}
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #1f2937; }
a { text-decoration: none; }

.app-header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  padding: 0 24px;
  height: 56px;
  gap: 8px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  color: #4f7cff;
  margin-right: 16px;
  flex-shrink: 0;
}
.logo-icon { font-size: 22px; }
.main-nav {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
  overflow-x: auto;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
  border-radius: 8px;
  white-space: nowrap;
  transition: all 0.2s;
}
.nav-item:hover { background: #f0f4ff; color: #4f7cff; }
.nav-active { background: #4f7cff; color: white !important; }
.nav-icon { font-size: 15px; }

.user-area { display: flex; align-items: center; gap: 10px; flex-shrink: 0; margin-left: 8px; }
.user-btn { font-size: 13px; color: #4f7cff; font-weight: 500; }
.login-btn {
  padding: 6px 16px;
  background: #4f7cff;
  color: white;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  border: none;
  cursor: pointer;
}
.logout-btn {
  padding: 6px 12px;
  background: transparent;
  color: #9ca3af;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}
.app-main { min-height: calc(100vh - 56px); }
.ph-back { display: flex; align-items: center; gap: 4px; background: none; border: none; color: #6b7280; font-size: 13px; cursor: pointer; padding: 6px 12px; border-radius: 6px; }
.ph-back:hover { background: #f0f4ff; color: #4f7cff; }
.ph-title { font-size: 16px; font-weight: 700; color: #4f7cff; }
.ph-spacer { flex: 1; }
.ph-link { font-size: 13px; color: #6b7280; padding: 6px 12px; border-radius: 6px; }
.ph-link:hover { background: #f0f4ff; color: #4f7cff; }
.ph-settings-wrap { position: relative; }
.ph-settings-btn { background: none; border: none; cursor: pointer; padding: 6px 8px; border-radius: 6px; color: #9ca3af; display: flex; align-items: center; }
.ph-settings-btn:hover { background: #f0f4ff; color: #4f7cff; }
.ph-settings-drop { position: absolute; top: 40px; right: 0; background: white; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); padding: 14px 16px; z-index: 200; width: 180px; }
.psd-item { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #374151; margin-bottom: 10px; gap: 12px; white-space: nowrap; }
@media (max-width: 768px) {
  .header-inner { padding: 0 12px; gap: 4px; }
  .logo-text { display: none; }
  .logo { margin-right: 4px; }
  .nav-item { padding: 6px 8px; font-size: 11px; gap: 2px; }
  .nav-icon { font-size: 13px; }
  .user-area { gap: 4px; }
  .user-btn { font-size: 11px; }
  .ph-title { font-size: 14px; }
  .ph-back { font-size: 11px; padding: 4px 8px; }
  .ph-link { font-size: 11px; padding: 4px 8px; }
  .ph-settings-drop { right: -60px; }
}
.global-watermark { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999; overflow: hidden; }
.global-watermark::before {
  content: 'fsbrm  fsbrm  fsbrm  fsbrm  fsbrm  fsbrm  fsbrm  fsbrm  fsbrm  fsbrm';
  position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
  font-size: 18px; color: rgba(0,0,0,0.03); font-weight: 700;
  white-space: pre-wrap; word-break: break-all; line-height: 120px;
  transform: rotate(-20deg); letter-spacing: 40px;
}
</style>
<style>
.img-watermark-wrap { position: relative; display: inline-block; max-width: 100%; }
.img-watermark-wrap img { display: block; max-width: 100%; }
.img-watermark-wrap::after {
  content: 'fsbrm'; position: absolute; bottom: 8px; right: 8px;
  color: rgba(255,255,255,0.8); font-size: 12px; font-weight: 700;
  background: rgba(0,0,0,0.35); padding: 2px 6px; border-radius: 4px;
  pointer-events: none; z-index: 5;
}
</style>