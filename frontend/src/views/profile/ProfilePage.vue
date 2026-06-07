<template>
  <div class="profile-page">
    <div class="profile-card card">
      <div class="profile-header">
        <el-avatar :size="80" :src="userStore.user?.avatar" icon="UserFilled" />
        <div class="profile-info">
          <h2>{{ userStore.user?.nickname || userStore.user?.username }}</h2>
          <p>@{{ userStore.user?.username }}</p>
          <el-tag size="small" :type="userStore.isAdmin ? 'danger' : ''">
            {{ userStore.isAdmin ? '管理员' : '普通用户' }}
          </el-tag>
        </div>
      </div>

      <el-divider />

      <!-- Learning Stats -->
      <div class="stats-row" v-if="stats">
        <div class="stat-item"><span class="stat-num">{{ stats.totalQuestions || 0 }}</span><span class="stat-lbl">总刷题</span></div>
        <div class="stat-item"><span class="stat-num">{{ stats.accuracy || 0 }}%</span><span class="stat-lbl">正确率</span></div>
        <div class="stat-item"><span class="stat-num">{{ stats.studyDays || 0 }}天</span><span class="stat-lbl">学习天数</span></div>
        <div class="stat-item"><span class="stat-num">{{ stats.streakDays || 0 }}天</span><span class="stat-lbl">连续打卡</span></div>
      </div>

      <el-divider />

      <el-form :model="form" label-width="80px" label-position="left">
        <el-form-item label="用户名">
          <el-input :model-value="userStore.user?.username" disabled />
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" placeholder="输入昵称" maxlength="20" show-word-limit />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="输入邮箱" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave" :loading="saving">保存修改</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import api from '@/api'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const saving = ref(false)
const stats = ref<any>(null)

const form = reactive({
  nickname: userStore.user?.nickname || '',
  email: (userStore.user as any)?.email || ''
})

onMounted(async () => {
  try {
    const res: any = await api.get('/dashboard')
    if (res.code === 200 && res.data?.overview) {
      stats.value = res.data.overview
    }
  } catch {}
})

async function handleSave() {
  saving.value = true
  try {
    await userStore.updateProfile({ nickname: form.nickname, email: form.email })
    ElMessage.success('保存成功')
  } catch {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.profile-page { max-width: 600px; margin: 0 auto; padding: 24px 20px; }
.profile-card { padding: 32px; }
.profile-header { display: flex; align-items: center; gap: 20px; }
.profile-info h2 { margin: 0 0 4px; font-size: 20px; }
.profile-info p { margin: 0 0 8px; color: #9ca3af; font-size: 14px; }
.stats-row { display: flex; gap: 0; }
.stat-item { flex: 1; text-align: center; padding: 12px 8px; }
.stat-num { display: block; font-size: 22px; font-weight: 700; color: #1f2937; }
.stat-lbl { display: block; font-size: 12px; color: #9ca3af; margin-top: 4px; }
</style>
