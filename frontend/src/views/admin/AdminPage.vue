<template>
  <div class="page-container">
    <h2 class="page-title">⚙️ 管理后台</h2>

    <div class="admin-cards">
      <div class="admin-card card" @click="$router.push('/admin/questions')">
        <div class="admin-icon">📋</div>
        <h3>题库管理</h3>
        <p>添加、编辑、删除题目，管理选项/视频/解析</p>
      </div>
      <div class="admin-card card" @click="$router.push('/admin/users')">
        <div class="admin-icon">👥</div>
        <h3>用户管理 & 数据仪表盘</h3>
        <p>用户管理、实时在线人数、刷题统计、每日卷王</p>
      </div>
    </div>

    <!-- Invite Code Management -->
    <div class="section-card card" style="margin-top:24px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
        <h3 style="margin:0">🔑 邀请码管理</h3>
        <div style="display:flex;gap:10px;align-items:center">
          <span style="font-size:13px;color:#9ca3af">剩余 {{ unusedCount }} 个</span>
          <el-input-number v-model="genCount" :min="1" :max="100" size="small" style="width:100px" />
          <el-button type="primary" size="small" @click="generateCodes" :loading="genLoading">生成邀请码</el-button>
        </div>
      </div>

      <el-table :data="inviteCodes" stripe size="small" v-loading="loading">
        <el-table-column prop="code" label="邀请码" width="200">
          <template #default="{row}">
            <code style="background:#f0f4ff;padding:2px 8px;border-radius:4px;font-size:12px">{{ row.code }}</code>
          </template>
        </el-table-column>
        <el-table-column prop="used" label="状态" width="100">
          <template #default="{row}">
            <el-tag :type="row.used ? 'info' : 'success'" size="small">{{ row.used ? '已使用' : '可用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="180" />
        <el-table-column label="操作" width="100">
          <template #default="{row}">
            <el-button type="danger" size="small" text @click="deleteCode(row)" :disabled="!!row.used">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="display:flex;justify-content:center;margin-top:12px">
        <el-pagination small layout="prev, pager, next" :total="total" :page-size="20" v-model:current-page="page" @current-change="loadCodes" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false); const genLoading = ref(false); const genCount = ref(5)
const inviteCodes = ref<any[]>([]); const page = ref(1); const total = ref(0); const unusedCount = ref(0)

async function loadCodes() {
  loading.value = true
  try {
    const res: any = await api.get('/admin/invite-codes', { params: { page: page.value, size: 20 } })
    if (res.code === 200) {
      inviteCodes.value = res.data.list || []; total.value = res.data.total || 0; unusedCount.value = res.data.unused || 0
    }
  } finally { loading.value = false }
}

async function generateCodes() {
  genLoading.value = true
  try {
    const res: any = await api.post('/admin/invite-codes/generate', { count: genCount.value })
    if (res.code === 200) { ElMessage.success(`成功生成 ${res.data.generated} 个邀请码`); loadCodes() }
  } finally { genLoading.value = false }
}

async function deleteCode(row: any) {
  try { await ElMessageBox.confirm('确定删除此邀请码？', '确认', { type: 'warning' }) } catch { return }
  try { const res: any = await api.delete(`/admin/invite-codes/${row.id}`); if (res.code === 200) { ElMessage.success('已删除'); loadCodes() } } catch {}
}

onMounted(loadCodes)
</script>

<style scoped>
.page-title { margin-bottom: 24px; }
.admin-cards { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.admin-card { padding: 32px 24px; text-align: center; cursor: pointer; transition: transform 0.2s; }
.admin-card:hover { transform: translateY(-4px); }
.admin-icon { font-size: 48px; margin-bottom: 16px; }
.admin-card h3 { margin-bottom: 8px; }
.admin-card p { font-size: 13px; color: var(--text-secondary); }
.section-card { padding: 20px 24px; }
@media (max-width: 768px) { .admin-cards { grid-template-columns: 1fr; } }
</style>
