<template>
  <div class="page-container">
    <div class="page-header">
      <h2>📝 错题本</h2>
      <el-button type="primary" @click="startRedo" :disabled="wrongQuestions.length === 0">重做全部错题</el-button>
    </div>

    <el-empty v-if="wrongQuestions.length === 0" description="太棒了！没有错题" />

    <div v-else class="wrong-list">
      <div v-for="wq in wrongQuestions" :key="wq.id" class="wrong-card card">
        <div class="wrong-info">
          <el-tag size="small" type="danger">错{{ wq.wrongCount }}次</el-tag>
          <span class="wrong-date">{{ formatDate(wq.lastWrongAt) }}</span>
        </div>
        <div class="wrong-content" v-if="wq.questionContent"><div v-html="wq.questionContent"></div></div>
        <div class="wrong-actions">
          <el-button size="small" type="primary" @click="$router.push(`/practice?chapterId=0&questionId=${wq.questionId}`)">重做</el-button>
          <el-button size="small" @click="removeWrong(wq)">移除</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const wrongQuestions = ref<any[]>([])

onMounted(async () => {
  try {
    const res: any = await api.get('/wrong')
    if (res.code === 200) wrongQuestions.value = res.data
  } catch {}
})

async function startRedo() {
  const res: any = await api.get('/wrong/practice')
  if (res.code === 200 && res.data.questions?.length > 0) {
    router.push('/practice?wrong=true')
  } else {
    ElMessage.warning('没有可重做的错题')
  }
}

async function removeWrong(wq: any) {
  try {
    await api.delete(`/wrong/${wq.questionId}`)
    wrongQuestions.value = wrongQuestions.value.filter(w => w.id !== wq.id)
    ElMessage.success('已移除')
  } catch {}
}

function formatDate(d: string) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }

.wrong-list { display: flex; flex-direction: column; gap: 12px; }
.wrong-card { padding: 20px; }
.wrong-info { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.wrong-date { font-size: 13px; color: var(--text-secondary); }
.wrong-content { font-size: 15px; line-height: 1.6; margin-bottom: 12px; padding: 12px; background: var(--bg-color); border-radius: 8px; }
.wrong-actions { display: flex; gap: 8px; }
</style>
