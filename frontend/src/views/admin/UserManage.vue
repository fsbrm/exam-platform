<template>
  <div class="page-container">
    <h2>👥 用户管理 & 数据仪表盘</h2>

    <!-- Overview Cards -->
    <div class="overview-cards">
      <div class="oc"><div class="oc-val">{{ overview.totalUsers }}</div><div class="oc-label">总用户</div></div>
      <div class="oc"><div class="oc-val">{{ overview.totalQuestions }}</div><div class="oc-label">总题目</div></div>
      <div class="oc"><div class="oc-val">{{ overview.totalAnswers }}</div><div class="oc-label">总答题数</div></div>
      <div class="oc"><div class="oc-val oc-green">{{ overview.todayAnswers }}</div><div class="oc-label">今日答题</div></div>
      <div class="oc"><div class="oc-val oc-blue">{{ overview.todayActiveUsers }}</div><div class="oc-label">今日活跃</div></div>
      <div class="oc"><div class="oc-val oc-orange">{{ onlineCount }}</div><div class="oc-label">在线用户</div></div>
    </div>

    <div class="flex-row">
      <!-- Daily Active Users Chart -->
      <div class="card chart-card"><h4>📈 近30天活跃用户</h4><div ref="activeChart" class="chart-box"></div></div>
      <!-- Daily Practice Chart -->
      <div class="card chart-card"><h4>📊 近30天刷题量</h4><div ref="practiceChart" class="chart-box"></div></div>
    </div>

    <div class="flex-row">
      <!-- Online Trend (24h) -->
      <div class="card chart-card"><h4>🕐 24h在线趋势</h4><div ref="onlineChart" class="chart-box"></div></div>
      <!-- Subject Distribution -->
      <div class="card chart-card"><h4>📚 科目刷题分布</h4><div ref="subjChart" class="chart-box"></div></div>
    </div>

    <div class="flex-row">
      <!-- Daily Top -->
      <div class="card" style="flex:1">
        <h4>🏆 每日卷王</h4>
        <div v-if="dailyTop.length===0" class="empty">今日暂无数据</div>
        <div v-for="(u,i) in dailyTop" :key="u.id" class="rank-row">
          <span class="rank-idx" :class="'r'+i">{{ i+1 }}</span>
          <span class="rank-name">{{ u.nickname||u.username }}</span>
          <span class="rank-cnt">{{ u.cnt }}题</span>
        </div>
      </div>
      <!-- Total Top -->
      <div class="card" style="flex:1">
        <h4>👑 刷题总榜 TOP10</h4>
        <div v-for="(u,i) in totalTop" :key="u.id" class="rank-row">
          <span class="rank-idx" :class="'r'+i">{{ i+1 }}</span>
          <span class="rank-name">{{ u.nickname||u.username }}</span>
          <span class="rank-cnt">{{ u.cnt }}题</span>
        </div>
      </div>
      <!-- Online Users -->
      <div class="card" style="flex:1">
        <h4>🟢 在线用户 (5min内有操作)</h4>
        <div v-if="onlineUsers.length===0" class="empty">暂无在线用户</div>
        <div v-for="u in onlineUsers" :key="u.id" class="rank-row">
          <span class="online-dot"></span>
          <span class="rank-name">{{ u.nickname||u.username }}</span>
          <span class="rank-time">{{ timeAgo(u.last_active) }}</span>
        </div>
      </div>
    </div>

    <!-- User List -->
    <div class="card" style="margin-top:20px">
      <h4>📋 用户列表</h4>
      <div style="display:flex;gap:10px;margin-bottom:12px">
        <el-input v-model="userKeyword" placeholder="搜索用户名/昵称/邮箱" size="small" style="width:240px" @change="loadUsers" clearable />
        <el-select v-model="userStatus" placeholder="状态" size="small" clearable @change="loadUsers"><el-option label="正常" :value="1"/><el-option label="禁用" :value="0"/></el-select>
      </div>
      <el-table :data="users" stripe size="small" v-loading="userLoading">
        <el-table-column prop="id" label="ID" width="50" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="nickname" label="昵称" width="120" />
        <el-table-column prop="email" label="邮箱" width="160" />
        <el-table-column prop="role" label="角色" width="80">
          <template #default="{row}"><el-tag :type="row.role==='ADMIN'?'danger':''" size="small">{{ row.role }}</el-tag></template>
        </el-table-column>
        <el-table-column label="状态" width="70">
          <template #default="{row}"><el-tag :type="row.status===0?'info':'success'" size="small">{{ row.status===0?'禁用':'正常' }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="totalDone" label="总刷题" width="80" />
        <el-table-column prop="lastActive" label="最后活跃" width="160" />
        <el-table-column label="操作" width="220">
          <template #default="{row}">
            <el-button size="small" @click="viewUser(row)">详情</el-button>
            <el-button size="small" :type="row.status===0?'success':'warning'" @click="toggleStatus(row)">{{ row.status===0?'启用':'禁用' }}</el-button>
            <el-button size="small" v-if="row.role!=='ADMIN'" type="danger" @click="changeRole(row,'ADMIN')">升管</el-button>
            <el-button size="small" v-if="row.role==='ADMIN'" @click="changeRole(row,'USER')">降权</el-button>
            <el-button size="small" plain @click="resetPwd(row)">改密</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-model:current-page="userPage" :page-size="15" :total="userTotal" layout="prev,pager,next" @current-change="loadUsers" style="margin-top:12px;justify-content:center" small />
    </div>

    <!-- User Detail Dialog -->
    <el-dialog v-model="showDetail" :title="'用户详情: '+detailUser?.nickname" width="700px">
      <div v-if="detailUser">
        <p><b>用户名:</b> {{ detailUser.username }} | <b>角色:</b> {{ detailUser.role }} | <b>刷题:</b> {{ detailUser.totalDone }} | <b>正确:</b> {{ detailUser.correctCount }}</p>
        <h4>最近答题记录</h4>
        <el-table :data="detailAnswers" size="small" max-height="300">
          <el-table-column prop="questionId" label="题号" width="70" />
          <el-table-column prop="subjectName" label="科目" width="100" />
          <el-table-column label="内容" show-overflow-tooltip><template #default="{row}"><span v-html="(row.content||'').substring(0,60)"></span></template></el-table-column>
          <el-table-column prop="userAnswer" label="用户答案" width="100" />
          <el-table-column label="结果" width="60"><template #default="{row}"><el-tag :type="row.isCorrect==1?'success':'danger'" size="small">{{ row.isCorrect==1?'✓':'✗' }}</el-tag></template></el-table-column>
          <el-table-column label="时间" width="160"><template #default="{row}">{{ row.answeredAt }}</template></el-table-column>
        </el-table>
        <div ref="userDailyChart" style="height:200px;margin-top:16px"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import api from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

// Overview
const overview = ref({totalUsers:0,totalQuestions:0,totalAnswers:0,todayAnswers:0,todayActiveUsers:0})
const onlineUsers = ref<any[]>([]); const onlineCount = ref(0)

// Charts refs
const activeChart = ref(); const practiceChart = ref(); const onlineChart = ref(); const subjChart = ref(); const userDailyChart = ref()

// Rankings
const dailyTop = ref<any[]>([]); const totalTop = ref<any[]>([])

// User list
const users = ref<any[]>([]); const userTotal = ref(0); const userPage = ref(1); const userLoading = ref(false)
const userKeyword = ref(''); const userStatus = ref<number|null>(null)

// User detail
const showDetail = ref(false); const detailUser = ref<any>(null); const detailAnswers = ref<any[]>([])

onMounted(async ()=>{ await loadAll(); setInterval(loadOnline,30000) })

async function loadAll(){
  const [ov,dau,dpr,ot,sd,dt,tt,ou] = await Promise.allSettled([
    api.get('/admin/analytics/overview'),api.get('/admin/analytics/daily-active'),
    api.get('/admin/analytics/daily-practice'),api.get('/admin/analytics/online-trend'),
    api.get('/admin/analytics/subject-distribution'),api.get('/admin/analytics/daily-top'),
    api.get('/admin/analytics/total-top'),api.get('/admin/analytics/online'),
  ])
  const g = (r:any)=>r.status==='fulfilled'?r.value?.data:null
  overview.value = g(ov)||overview.value
  dailyTop.value = g(dt)||[]; totalTop.value = g(tt)||[]; onlineUsers.value = g(ou)||[]; onlineCount.value = onlineUsers.value.length

  await nextTick()
  const cm = (ref:any,d:any,t:string,leg:string,sm:boolean=false)=> {
    if(!ref||!d?.length)return; const c=echarts.init(ref);
    c.setOption({tooltip:{trigger:'axis'},grid:{left:40,right:10,top:20,bottom:30},
      xAxis:{type:'category',data:d.map((x:any)=>x.date||x.hour),axisLabel:{fontSize:10}},
      yAxis:{type:'value',axisLabel:{fontSize:10}},series:[{name:leg,type:t,data:d.map((x:any)=>x.count||x.cnt),smooth:sm,areaStyle:t==='line'?{opacity:0.3}:undefined,itemStyle:{color:'#4f7cff'}}]})
  }
  const pie = (ref:any,d:any)=>{
    if(!ref||!d?.length)return; const c=echarts.init(ref);
    c.setOption({tooltip:{trigger:'item'},series:[{type:'pie',radius:['40%','70%'],data:d.map((x:any)=>({name:x.name,value:x.cnt})),label:{fontSize:10}}]})
  }
  cm(activeChart.value,g(dau),'line','活跃用户',true)
  cm(practiceChart.value,g(dpr),'bar','刷题量')
  cm(onlineChart.value,g(ot),'area','在线人数',true)
  pie(subjChart.value,g(sd))
  loadUsers()
}
async function loadOnline(){
  try{const r:any=await api.get('/admin/analytics/online');if(r.code===200){onlineUsers.value=r.data||[];onlineCount.value=onlineUsers.value.length}}catch{}
}

async function loadUsers(){
  userLoading.value=true
  try{const r:any=await api.get('/admin/users',{params:{page:userPage.value,size:15,keyword:userKeyword.value||undefined,status:userStatus.value!=null?userStatus.value:undefined}})
  if(r.code===200){users.value=r.data.records||[];userTotal.value=r.data.total||0}}finally{userLoading.value=false}
}

async function toggleStatus(row:any){
  const ns = row.status===0?1:0
  try{await api.put(`/admin/users/${row.id}/status`,{status:ns}); row.status=ns; ElMessage.success(ns===1?'已启用':'已禁用')}catch{}
}
async function changeRole(row:any,role:string){
  try{await api.put(`/admin/users/${row.id}/role`,{role}); row.role=role; ElMessage.success('角色已更新')}catch{}
}
async function resetPwd(row:any){
  try{const { value } = await ElMessageBox.prompt(`请输入 ${row.username} 的新密码（至少6位）`,'重置密码',{confirmButtonText:'确定',cancelButtonText:'取消',inputType:'text',inputValidator:(v:string)=>{if(!v||v.length<6)return'密码至少6位';return true}}); if(!value)return
  await api.put(`/admin/users/${row.id}/password`,{password:value}); ElMessage.success('密码已重置')}catch{}
}
async function viewUser(u:any){
  try{const r:any=await api.get(`/admin/users/${u.id}`); if(r.code===200){
    detailUser.value=r.data; detailAnswers.value=r.data.recentAnswers||[]
    showDetail.value=true
    await nextTick()
    const d=r.data.dailyActivity||[]
    if(userDailyChart.value&&d.length){const c=echarts.init(userDailyChart.value)
      c.setOption({tooltip:{trigger:'axis'},grid:{left:40,right:10,top:10,bottom:30},
        xAxis:{type:'category',data:d.map((x:any)=>x.date),axisLabel:{fontSize:9}},
        yAxis:{type:'value',axisLabel:{fontSize:9}},series:[{name:'刷题数',type:'bar',data:d.map((x:any)=>x.count),itemStyle:{color:'#4f7cff'}}]})}
  }}catch{}
}
function timeAgo(t:string){if(!t)return'';const d=(Date.now()-new Date(t).getTime())/1000;return d<60?Math.floor(d)+'秒前':d<3600?Math.floor(d/60)+'分钟前':Math.floor(d/3600)+'小时前'}
</script>

<style scoped>
h2{margin-bottom:16px}h4{margin:0 0 10px;font-size:14px}
.overview-cards{display:flex;gap:14px;margin-bottom:20px;flex-wrap:wrap}
.oc{flex:1;min-width:100px;background:white;padding:16px;border-radius:10px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.oc-val{font-size:28px;font-weight:800;color:#1f2937}.oc-label{font-size:12px;color:#9ca3af;margin-top:4px}
.oc-green{color:#10b981}.oc-blue{color:#3b82f6}.oc-orange{color:#f59e0b}
.flex-row{display:flex;gap:16px;margin-bottom:16px}
.chart-card{flex:1;padding:16px}.chart-box{height:220px}
.rank-row{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #f3f4f6;font-size:13px}
.rank-idx{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;background:#f3f4f6}.rank-idx.r0{background:#fbbf24;color:white}.rank-idx.r1{background:#9ca3af;color:white}.rank-idx.r2{background:#d97706;color:white}
.rank-name{flex:1;color:#374151}.rank-cnt{color:#6b7280;font-weight:600}.rank-time{font-size:11px;color:#9ca3af}
.online-dot{width:8px;height:8px;border-radius:50%;background:#10b981}
.empty{color:#9ca3af;font-size:13px;text-align:center;padding:20px}
.card{padding:16px;background:white;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
</style>
