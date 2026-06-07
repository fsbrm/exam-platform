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
            <div class="ph-settings-drop" v-if="showSettings">
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
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter, useRoute } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

// Practice settings
const showSettings = ref(false)
const feedbackEnabled = ref(localStorage.getItem('practice_feedback') === 'true')
const keyboardEnabled = ref(localStorage.getItem('practice_keyboard') === 'true')
const comboEnabled = ref(localStorage.getItem('practice_combo') === 'true')
function saveSetting() {
  localStorage.setItem('practice_feedback', String(feedbackEnabled.value))
  localStorage.setItem('practice_keyboard', String(keyboardEnabled.value))
  localStorage.setItem('practice_combo', String(comboEnabled.value))
}

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
</style>