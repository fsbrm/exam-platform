<template>
  <div class="page-container">
    <div class="page-header">
      <h2>📋 题库管理</h2>
      <el-button type="primary" @click="showDialog = true; editingQuestion = null">添加题目</el-button>
    </div>

    <el-table :data="questions" border stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="content" label="题目内容" show-overflow-tooltip />
      <el-table-column prop="type" label="题型" width="80">
        <template #default="{ row }">{{ ({SINGLE:'单选',MULTI:'多选',JUDGE:'判断',FILL:'填空'} as Record<string, string>)[row.type] }}</template>
      </el-table-column>
      <el-table-column prop="difficulty" label="难度" width="80">
        <template #default="{ row }">
          <el-tag :type="({EASY:'success',MEDIUM:'warning',HARD:'danger'} as Record<string, string>)[row.difficulty]" size="small">
            {{ ({EASY:'简单',MEDIUM:'中等',HARD:'困难'} as Record<string, string>)[row.difficulty] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="answer" label="答案" width="100" show-overflow-tooltip />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" @click="editQuestion(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteQuestion(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="pageNum" :page-size="10" :total="total"
      layout="prev, pager, next" @current-change="loadQuestions"
      style="margin-top: 20px; justify-content: center;"
    />

    <!-- Add/Edit Dialog -->
    <el-dialog v-model="showDialog" :title="editingQuestion ? '编辑题目' : '添加题目'" width="700px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="科目">
          <el-select v-model="form.subjectId" placeholder="选择科目">
            <el-option label="408 计算机综合" :value="1" />
            <el-option label="高等数学" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="题型">
          <el-select v-model="form.type">
            <el-option label="单选题" value="SINGLE" />
            <el-option label="多选题" value="MULTI" />
            <el-option label="判断题" value="JUDGE" />
            <el-option label="填空题" value="FILL" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="form.difficulty">
            <el-option label="简单" value="EASY" />
            <el-option label="中等" value="MEDIUM" />
            <el-option label="困难" value="HARD" />
          </el-select>
        </el-form-item>
        <el-form-item label="题目内容">
          <el-input v-model="form.content" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="选项JSON" v-if="['SINGLE','MULTI'].includes(form.type)">
          <el-input v-model="form.options" type="textarea" :rows="4" placeholder='[{"key":"A","value":"选项A"},{"key":"B","value":"选项B"}]' />
        </el-form-item>
        <el-form-item label="正确答案">
          <el-input v-model="form.answer" placeholder="单选题: A; 多选题: A,B; 判断题: T/F; 填空题: 具体答案" />
        </el-form-item>
        <el-form-item label="解析">
          <el-input v-model="form.analysis" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveQuestion" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const questions = ref<any[]>([])
const pageNum = ref(1)
const total = ref(0)
const showDialog = ref(false)
const saving = ref(false)
const editingQuestion = ref<any>(null)
const form = ref({
  subjectId: 1, chapterId: 1, type: 'SINGLE', difficulty: 'MEDIUM',
  content: '', options: '', answer: '', analysis: ''
})

onMounted(() => loadQuestions())

async function loadQuestions() {
  loading.value = true
  try {
    const res: any = await api.get('/admin/questions', { params: { pageNum: pageNum.value, pageSize: 10 } })
    if (res.code === 200) {
      questions.value = res.data.records
      total.value = res.data.total
    }
  } finally { loading.value = false }
}

function editQuestion(q: any) {
  editingQuestion.value = q
  form.value = { ...q }
  showDialog.value = true
}

async function saveQuestion() {
  saving.value = true
  try {
    if (editingQuestion.value) {
      await api.put(`/admin/questions/${editingQuestion.value.id}`, form.value)
    } else {
      await api.post('/admin/questions', form.value)
    }
    ElMessage.success('保存成功')
    showDialog.value = false
    resetForm()
    loadQuestions()
  } catch {} finally { saving.value = false }
}

async function deleteQuestion(q: any) {
  await ElMessageBox.confirm('确定删除该题目？', '确认删除', { type: 'warning' })
  try {
    await api.delete(`/admin/questions/${q.id}`)
    ElMessage.success('删除成功')
    loadQuestions()
  } catch {}
}

function resetForm() {
  editingQuestion.value = null
  form.value = { subjectId: 1, chapterId: 1, type: 'SINGLE', difficulty: 'MEDIUM', content: '', options: '', answer: '', analysis: '' }
}
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
</style>
