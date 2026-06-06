<template>
  <div class="page-container">
    <div class="page-header">
      <h2>📋 题库管理 <span class="sub">共 {{ total }} 题</span></h2>
      <el-button type="primary" @click="openAdd">+ 添加题目</el-button>
    </div>

    <!-- Filters -->
    <div class="qm-filters">
      <el-select v-model="fSubject" placeholder="科目" clearable size="small" @change="loadQ">
        <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" />
      </el-select>
      <el-select v-model="fType" placeholder="题型" clearable size="small" @change="loadQ">
        <el-option label="单选" value="SINGLE" /><el-option label="多选" value="MULTI" />
        <el-option label="判断" value="JUDGE" /><el-option label="综合" value="COMPREHENSIVE" />
      </el-select>
      <el-select v-model="fDifficulty" placeholder="难度" clearable size="small" @change="loadQ">
        <el-option label="简单" value="EASY" /><el-option label="中等" value="MEDIUM" /><el-option label="困难" value="HARD" />
      </el-select>
      <el-input v-model="fKeyword" placeholder="搜索题目内容..." size="small" style="width:200px" clearable @change="loadQ" @clear="loadQ" />
      <el-select v-model="fChapter" placeholder="章节" clearable size="small" @change="loadQ">
        <el-option v-for="c in allChapters" :key="c.id" :label="c.name" :value="c.id" />
      </el-select>
    </div>

    <el-table :data="questions" border stripe v-loading="loading" size="small">
      <el-table-column prop="id" label="ID" width="50" />
      <el-table-column prop="content" label="题目内容" show-overflow-tooltip min-width="200">
        <template #default="{row}"><span v-html="row.content?.substring(0,80)"></span></template>
      </el-table-column>
      <el-table-column label="科目" width="80">
        <template #default="{row}">{{ subjectName(row.subjectId) }}</template>
      </el-table-column>
      <el-table-column label="题型" width="60">
        <template #default="{row}">{{ typeMap[row.type] }}</template>
      </el-table-column>
      <el-table-column label="难度" width="60">
        <template #default="{row}"><el-tag :type="diffType(row.difficulty)" size="small">{{ diffMap[row.difficulty] }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="answer" label="答案" width="80" show-overflow-tooltip />
      <el-table-column label="操作" width="140">
        <template #default="{row}">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="del(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination v-model:current-page="pageNum" :page-size="15" :total="total"
      layout="prev, pager, next" @current-change="loadQ" style="margin-top:16px;justify-content:center" />

    <!-- Edit Dialog -->
    <el-dialog v-model="showDlg" :title="editing?.id ? '编辑题目 #'+editing.id : '添加题目'" width="800px" @close="resetForm">
      <el-form :model="form" label-width="80px" size="small">
        <el-row :gutter="12">
          <el-col :span="8">
            <el-form-item label="科目"><el-select v-model="form.subjectId" @change="onSubjChange"><el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" /></el-select></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="章节"><el-select v-model="form.chapterId" :disabled="!form.subjectId"><el-option v-for="c in chOptions" :key="c.id" :label="c.name" :value="c.id" /></el-select></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="年份"><el-input-number v-model="form.year" :min="2000" :max="2030" controls-position="right" /></el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="12">
          <el-col :span="8">
            <el-form-item label="题型"><el-select v-model="form.type"><el-option label="单选" value="SINGLE" /><el-option label="多选" value="MULTI" /><el-option label="判断" value="JUDGE" /><el-option label="综合" value="COMPREHENSIVE" /><el-option label="填空" value="FILL" /></el-select></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="难度"><el-select v-model="form.difficulty"><el-option label="简单" value="EASY" /><el-option label="中等" value="MEDIUM" /><el-option label="困难" value="HARD" /></el-select></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="配图URL"><el-input v-model="form.image" placeholder="可选" /></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="题目内容"><el-input v-model="form.content" type="textarea" :rows="4" /></el-form-item>
        <el-form-item label="选项" v-if="['SINGLE','MULTI'].includes(form.type)">
          <div class="opts-editor">
            <div v-for="(opt,i) in optsList" :key="i" class="opts-row">
              <span class="opts-key">{{ opt.key }}</span>
              <el-input v-model="opt.value" :placeholder="'选项 '+opt.key" size="small" @input="syncOpts" />
              <el-button size="small" text type="danger" @click="removeOpt(i)" :disabled="optsList.length<=2">✕</el-button>
            </div>
            <el-button size="small" text @click="addOpt" :disabled="optsList.length>=8">+ 添加选项</el-button>
          </div>
        </el-form-item>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="正确答案"><el-input v-model="form.answer" placeholder="单选:A 多选:A,B 判断:T/F" /></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="推荐视频"><el-input v-model="form.videoUrl" placeholder="视频链接(可选)" /></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="解析"><el-input v-model="form.analysis" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="form.statusBool" active-text="启用" inactive-text="禁用" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDlg=false">取消</el-button>
        <el-button type="primary" @click="save" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false), saving = ref(false), showDlg = ref(false)
const questions = ref<any[]>([]), total = ref(0), pageNum = ref(1)
const subjects = ref<any[]>([]), allChapters = ref<any[]>([])
const fSubject = ref<number|null>(null), fType = ref(''), fDifficulty = ref(''), fKeyword = ref(''), fChapter = ref<number|null>(null)
const editing = ref<any>(null)
const form = ref({
  subjectId: 1 as number|null, chapterId: null as number|null, year: null as number|null,
  type: 'SINGLE', difficulty: 'MEDIUM', content: '', answer: '',
  analysis: '', image: '', videoUrl: '', statusBool: true
})
const optsList = ref<{key:string,value:string}[]>([{key:'A',value:''},{key:'B',value:''},{key:'C',value:''},{key:'D',value:''}])

const chOptions = computed(() => form.value.subjectId ? allChapters.value.filter((c:any)=>c.subjectId===form.value.subjectId) : [])

const typeMap: Record<string,string> = {SINGLE:'单选',MULTI:'多选',JUDGE:'判断',COMPREHENSIVE:'综合',FILL:'填空'}
const diffMap: Record<string,string> = {EASY:'简单',MEDIUM:'中等',HARD:'困难'}
function diffType(d:string){ return {EASY:'success',MEDIUM:'warning',HARD:'danger'}[d] || 'info' }
function subjectName(id:number){ return subjects.value.find((s:any)=>s.id===id)?.name || '' }

onMounted(async ()=>{
  const [sRes,chRes] = await Promise.allSettled([api.get('/subjects'), api.get('/knowledge/tree')])
  if(sRes.status==='fulfilled' && (sRes.value as any).code===200) subjects.value = (sRes.value as any).data||[]
  if(chRes.status==='fulfilled' && (chRes.value as any).code===200){
    const tree = (chRes.value as any).data?.tree||[]
    const chs:any[] = []; tree.forEach((s:any)=>(s.chapters||[]).forEach((c:any)=>chs.push({...c,subjectId:s.id}))); allChapters.value = chs
  }
  loadQ()
})

async function loadQ(){
  loading.value = true
  try{
    const params:any = {pageNum:pageNum.value,pageSize:15}
    if(fSubject.value) params.subjectId = fSubject.value
    if(fType.value) params.type = fType.value
    if(fDifficulty.value) params.difficulty = fDifficulty.value
    if(fKeyword.value) params.keyword = fKeyword.value
    if(fChapter.value) params.chapterId = fChapter.value
    const res:any = await api.get('/admin/questions',{params})
    if(res.code===200){ questions.value = res.data.records||[]; total.value = res.data.total||0 }
  }finally{ loading.value = false }
}

function openAdd(){ editing.value=null; resetForm(); showDlg.value=true }
function openEdit(q:any){
  editing.value = q
  form.value = {subjectId:q.subjectId,chapterId:q.chapterId,year:q.year,type:q.type,difficulty:q.difficulty,content:q.content||'',answer:q.answer||'',analysis:q.analysis||'',image:q.image||'',videoUrl:q.videoUrl||'',statusBool:q.status!==0}
  if(q.options){ try{optsList.value=JSON.parse(q.options)}catch{optsList.value=[{key:'A',value:''},{key:'B',value:''},{key:'C',value:''},{key:'D',value:''}]} }
  else optsList.value = [{key:'A',value:''},{key:'B',value:''},{key:'C',value:''},{key:'D',value:''}]
  showDlg.value=true
}
function resetForm(){
  editing.value=null
  form.value = {subjectId:1,chapterId:null,year:null,type:'SINGLE',difficulty:'MEDIUM',content:'',answer:'',analysis:'',image:'',videoUrl:'',statusBool:true}
  optsList.value = [{key:'A',value:''},{key:'B',value:''},{key:'C',value:''},{key:'D',value:''}]
}
function syncOpts(){ form.value.options = JSON.stringify(optsList.value.filter(o=>o.value)) }
function addOpt(){ const k = String.fromCharCode(65+optsList.value.length); optsList.value.push({key:k,value:''}) }
function removeOpt(i:number){ optsList.value.splice(i,1); syncOpts() }
function onSubjChange(){ form.value.chapterId = null }

async function save(){
  saving.value = true
  try{
    const payload:any = {...form.value, status: form.value.statusBool?1:0, options: JSON.stringify(optsList.value.filter(o=>o.value))}
    delete payload.statusBool
    if(editing.value?.id){
      await api.put(`/admin/questions/${editing.value.id}`,payload)
      ElMessage.success('题目已更新')
    }else{
      await api.post('/admin/questions',payload)
      ElMessage.success('题目已添加')
    }
    showDlg.value=false; loadQ()
  }catch{}finally{saving.value=false}
}

async function del(q:any){
  try{await ElMessageBox.confirm('确定删除题目 #'+q.id+'？','确认删除',{type:'warning'})}catch{return}
  try{await api.delete(`/admin/questions/${q.id}`); ElMessage.success('已删除'); loadQ()}catch{}
}
</script>

<style scoped>
.page-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.page-header h2{margin:0}.sub{font-size:14px;color:#9ca3af;font-weight:400;margin-left:8px}
.qm-filters{display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.opts-editor{display:flex;flex-direction:column;gap:6px;width:100%}
.opts-row{display:flex;align-items:center;gap:8px}.opts-key{font-weight:700;width:24px;text-align:center;color:#4f7cff}
</style>
