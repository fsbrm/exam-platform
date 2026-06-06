<template>
  <div class="page-container">
    <div class="profile-card card">
      <div class="profile-header">
        <el-avatar :size="80" icon="UserFilled" />
        <div class="profile-info">
          <h2>{{ userStore.user?.nickname || userStore.user?.username }}</h2>
          <p>@{{ userStore.user?.username }}</p>
          <el-tag size="small">{{ userStore.user?.role === 'ADMIN' ? '管理员' : '普通用户' }}</el-tag>
        </div>
      </div>

      <el-divider />

      <el-descriptions title="账号信息" :column="2" border>
        <el-descriptions-item label="用户名">{{ userStore.user?.username }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ userStore.user?.email || '未设置' }}</el-descriptions-item>
        <el-descriptions-item label="角色">{{ userStore.user?.role === 'ADMIN' ? '管理员' : '用户' }}</el-descriptions-item>
        <el-descriptions-item label="注册时间">-</el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
</script>

<style scoped>
.profile-card { max-width: 600px; margin: 0 auto; padding: 32px; }
.profile-header { display: flex; align-items: center; gap: 20px; margin-bottom: 8px; }
.profile-info h2 { font-size: 22px; margin-bottom: 4px; }
.profile-info p { color: var(--text-secondary); font-size: 14px; margin-bottom: 8px; }
</style>
