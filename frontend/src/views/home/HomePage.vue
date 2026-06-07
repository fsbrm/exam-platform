<template>
  <div class="home-page">
    <section class="hero">
      <h1>408 真题刷题平台</h1>
      <p>2009-2026 · 四大学科 144 知识点全覆盖</p>
      <div class="hero-cta" @click="$router.push('/practice')">
        <span>立即刷题</span>
        <span class="cta-arrow">→</span>
      </div>
    </section>

    <div class="main-layout">
      <div class="main-col">
        <template v-if="userStore.isLoggedIn">
          <div class="two-col">
            <div class="section-card">
              <h3>🔥 今日概况</h3>
              <div v-if="todayCount > 0" class="today-box">
                <div class="today-big">{{ todayCount }}<span>题</span></div>
                <div class="today-detail"><span class="tc">{{ todayCorrect }} 正确</span><span class="sep">·</span><span class="te">{{ todayCount - todayCorrect }} 错误</span><span class="sep">·</span><span>正确率 {{ todayCount>0 ? Math.round(todayCorrect/todayCount*100) : 0 }}%</span></div>
              </div>
              <div v-else class="today-box dim"><div class="today-big">0<span>题</span></div><div class="today-detail">今天还没刷题，去练几道吧~</div></div>
            </div>
            <div class="section-card">
              <h3>📊 科目掌握度</h3>
              <div class="subj-bars">
                <div v-for="s in subjectBars" :key="s.name" class="sb-row">
                  <div class="sb-hd"><span class="sb-dot" :style="{background:s.color}"></span><span class="sb-name">{{ s.name }}</span><span class="sb-pct">{{ s.mastery }}%</span></div>
                  <div class="sb-bar"><div class="sb-fill" :style="{width:s.mastery+'%',background:s.color}"></div></div>
                  <div class="sb-sub">已做 {{ s.done }}/{{ s.total }} 题 · 正确 {{ s.correct }} 题</div>
                </div>
              </div>
            </div>
          </div>

          <div class="section-card" v-if="weakPoints.length > 0">
            <h3>🎯 优先攻克</h3>
            <div class="weak-row">
              <div v-for="wp in weakPoints.slice(0,6)" :key="wp.id" class="wp-tag" @click="$router.push(`/practice?knowledgeId=${wp.id}&from=knowledge`)">
                <span class="wp-cat" :style="{background:catColor(wp.category)}">{{ wp.category }}</span>
                <span class="wp-name">{{ wp.name }}</span>
                <span class="wp-ratio">{{ wp.correct_count||0 }}/{{ wp.done_count||0 }}</span>
              </div>
            </div>
          </div>
        </template>

        <section v-else class="guest-box">
          <div class="guest-icon">🎓</div>
          <p>登录后追踪学习数据</p>
          <p class="gsub">打卡记录 · 刷题统计 · 薄弱分析</p>
          <el-button type="primary" size="large" round @click="$router.push('/login')">立即登录</el-button>
        </section>

        <section class="section-card" style="margin-top:16px">
          <h3>📚 考试科目</h3>
          <div class="subj-cards">
            <div v-for="s in subjects" :key="s.name" class="sc-card" :style="{'--sc':s.color}">
              <div class="sc-top"><span class="sc-ico">{{ s.icon }}</span><span class="sc-name">{{ s.name }}</span></div>
              <div class="sc-info"><span>{{ s.kpCount }}知识点</span><span>~{{ s.qCount }}题</span></div>
            </div>
          </div>
        </section>
      </div>

      <div class="side-col" v-if="userStore.isLoggedIn">
        <div class="side-card">
          <div class="cal-nav"><span class="cal-arrow" @click="prevMonth">◀</span><span class="cal-month-label">{{ calYear }}年 {{ calMonth }}月</span><span class="cal-arrow" @click="nextMonth">▶</span></div>
          <div class="cal-weekdays"><span v-for="wd in weekDays" :key="wd">{{ wd }}</span></div>
          <div class="cal-grid"><div v-for="(d,i) in calMonthDays" :key="i" class="cal-cell" :class="[d.inMonth?'lvl'+d.level:'',!d.inMonth?'out-month':'']" :title="d.inMonth?d.label:''"><span class="cal-day">{{ d.day }}</span></div></div>
          <div class="cal-legend"><span>少</span><span class="cl-dot lvl0"></span><span class="cl-dot lvl1"></span><span class="cl-dot lvl2"></span><span class="cl-dot lvl3"></span><span class="cl-dot lvl4"></span><span>多</span></div>
          <div class="cal-footer">🔥 连续 {{ overview.streakDays||0 }} 天 · 📅 累计 {{ overview.studyDays||0 }} 天</div>
        </div>

        <!-- Leaderboard -->
        <div class="side-card" style="margin-top:10px">
          <h4>🏆 排行榜</h4>
          <div class="lb-tabs">
            <span :class="{active:lbTab==='day'}" @click="lbTab='day'">日题数</span>
            <span :class="{active:lbTab==='acc'}" @click="lbTab='acc'">日正确率</span>
            <span :class="{active:lbTab==='total'}" @click="lbTab='total'">总题量</span>
          </div>
          <div class="lb-list">
            <div v-for="(u,i) in lbData" :key="u.id" class="lb-row">
              <span class="lb-idx" :class="'r'+i">{{ i+1 }}</span>
              <span class="lb-name">{{ u.nickname||u.username }}</span>
              <span class="lb-val">{{ u.cnt }}题</span>
            </div>
            <div v-if="lbData.length===0" class="lb-empty">暂无数据</div>
          </div>
        </div>

        <div class="side-card" style="margin-top:10px">
          <h4>快捷入口</h4>
          <div class="side-links">
            <div class="sl-item" @click="$router.push('/papers')"><span>📋</span>真题矩阵</div>
            <div class="sl-item" @click="$router.push('/knowledge')"><span>🕸️</span>知识森林</div>
            <div class="sl-item" @click="$router.push('/analytics')"><span>📊</span>学习分析</div>
            <div class="sl-item" @click="$router.push('/wrong')"><span>📝</span>错题本</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const userStore = useUserStore()

const overview = ref<any>({})
const todayCount = ref(0)
const todayCorrect = ref(0)
const weakPoints = ref<any[]>([])
const lbTab = ref('day')
const lbData = ref<any[]>([])
const subjectBars = ref<any[]>([])
const subjects = ref<any[]>([
  { name: '数据结构', icon: '📊', color: '#4f7cff', kpCount: 39, qCount: 219 },
  { name: '计算机组成原理', icon: '💻', color: '#fa8c16', kpCount: 37, qCount: 206 },
  { name: '操作系统', icon: '⚙️', color: '#52c41a', kpCount: 30, qCount: 213 },
  { name: '计算机网络', icon: '🌐', color: '#9c27b0', kpCount: 38, qCount: 150 }
])

const calYear = ref(new Date().getFullYear())
const calMonth = ref(new Date().getMonth() + 1)
const weekDays = ['日','一','二','三','四','五','六']

const calMonthDays = computed(() => {
  const year = calYear.value; const month = calMonth.value
  const firstDay = new Date(year, month-1, 1).getDay()
  const daysInMonth = new Date(year, month, 0).getDate()
  const days: any[] = []
  for (let i = 0; i < firstDay; i++) days.push({ day: '', inMonth: false, level: 0, label: '' })
  for (let d = 1; d <= daysInMonth; d++) {
    const key = `${year}-${String(month).padStart(2,'0')}-${String(d).padStart(2,'0')}`
    const count = heatmapData.value[key] || 0
    const level = count === 0 ? 0 : count <= 3 ? 1 : count <= 8 ? 2 : count <= 15 ? 3 : 4
    days.push({ day: d, inMonth: true, level, label: `${key}: ${count}题` })
  }
  return days
})

const heatmapData = ref<Record<string, number>>({})

function prevMonth() {
  if (calMonth.value === 1) { calYear.value--; calMonth.value = 12 }
  else calMonth.value--
}
function nextMonth() {
  if (calMonth.value === 12) { calYear.value++; calMonth.value = 1 }
  else calMonth.value++
}

function catColor(c: string) {
  const map: Record<string,string> = { '数据结构':'#4f7cff','计算机组成原理':'#fa8c16','操作系统':'#52c41a','计算机网络':'#9c27b0' }
  return map[c] || '#999'
}

onMounted(async () => {
  try {
    const res: any = await api.get('/dashboard')
    if (res.code === 200) {
      overview.value = res.data.overview || {}
      todayCount.value = res.data.todayCount || 0
      todayCorrect.value = res.data.todayCorrect || 0
      heatmapData.value = res.data.heatmap || {}
      const raw = res.data.subjectStats || []
      subjectBars.value = raw.map((s: any) => ({
        name: s.name, color: catColor(s.name),
        done: s.doneCount || 0, total: s.totalCount || 0,
        correct: s.correctCount || 0,
        mastery: s.totalCount > 0 ? Math.round(s.correctCount / s.totalCount * 100) : 0
      }))
    }
  } catch {}

  // Fetch subject IDs dynamically for weakness query
  let subjectIds: number[] = [1, 2, 3, 4]
  try {
    const subjRes: any = await api.get('/subjects')
    if (subjRes.code === 200 && subjRes.data?.length) {
      subjectIds = subjRes.data.map((s: any) => s.id)
    }
  } catch {}
  const weakAll: any[] = []
  for (const sid of subjectIds) {
    try {
      const wr: any = await api.get('/knowledge/weakness', { params: { subjectId: sid } })
      if (wr.code === 200) weakAll.push(...(wr.data || []))
    } catch {}
  }
  weakPoints.value = weakAll.sort((a: any, b: any) =>
    ((b.done_count||0)-(b.correct_count||0)) - ((a.done_count||0)-(a.correct_count||0))
  ).slice(0, 6)
  loadLeaderboard()
})
async function loadLeaderboard() {
  try{const r:any=await api.get('/admin/analytics/'+(lbTab.value==='day'?'daily-top':lbTab.value==='acc'?'daily-accuracy':'total-top'));if(r.code===200)lbData.value=r.data||[]}catch{lbData.value=[]}
}
watch(lbTab, loadLeaderboard)
</script>

<style scoped>
.home-page{max-width:1200px;margin:0 auto;padding:16px 20px}
.hero{text-align:center;padding:30px 0 20px}
.hero h1{font-size:28px;font-weight:800;color:#1f2937;margin-bottom:4px}
.hero p{font-size:14px;color:#9ca3af}
.hero-cta{display:inline-flex;align-items:center;gap:8px;margin-top:16px;padding:10px 28px;background:linear-gradient(135deg,#4f7cff,#6366f1);color:white;border-radius:50px;cursor:pointer;font-size:16px;font-weight:600;transition:all .3s;box-shadow:0 4px 16px rgba(79,124,255,.3)}
.hero-cta:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(79,124,255,.45)}
.cta-arrow{display:inline-block;animation:cta-bounce .8s ease-in-out infinite}
@keyframes cta-bounce{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}
.main-layout{display:grid;grid-template-columns:1fr 280px;gap:16px}
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px;position:relative}
.stats-row.clickable{cursor:pointer;transition:all .2s}.stats-row.clickable:hover{transform:translateY(-2px)}
.stats-row.clickable:hover .stat-card{box-shadow:0 4px 12px rgba(0,0,0,.08)}
.stat-card{background:white;border-radius:14px;padding:16px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.04);transition:box-shadow .2s}
.stats-arrow{position:absolute;right:-8px;top:50%;transform:translateY(-50%);font-size:13px;color:#9ca3af;opacity:0;transition:all .2s;pointer-events:none}
.stats-row.clickable:hover .stats-arrow{opacity:1;right:-32px;color:#4f7cff}
.stat-card.c1 .sc-num{color:#4f7cff}.stat-card.c2 .sc-num{color:#52c41a}.stat-card.c3 .sc-num{color:#fa8c16}.stat-card.c4 .sc-num{color:#9c27b0}
.sc-num{font-size:32px;font-weight:800;display:flex;align-items:baseline;justify-content:center;gap:2px}
.sc-sfx{font-size:16px;font-weight:500;color:#9ca3af}
.sc-unit{font-size:12px;color:#9ca3af;margin-top:2px}
.section-card{background:white;border-radius:14px;padding:18px 22px;box-shadow:0 1px 3px rgba(0,0,0,.04);margin-bottom:14px}
.section-card h3{font-size:15px;margin-bottom:12px;color:#1f2937}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.today-box{text-align:center;padding:8px 0}
.today-big{font-size:52px;font-weight:800;color:#4f7cff;line-height:1}
.today-big span{font-size:16px;font-weight:500;color:#9ca3af}
.today-box.dim .today-big{color:#e5e7eb}
.today-detail{font-size:13px;color:#6b7280;margin-top:6px}
.today-detail .sep{margin:0 5px;color:#d1d5db}
.tc{color:#52c41a}.te{color:#ff4d4f}
.today-box.dim .today-detail{color:#9ca3af}
.subj-bars{display:flex;flex-direction:column;gap:14px}
.sb-hd{display:flex;align-items:center;gap:7px;margin-bottom:3px}
.sb-dot{width:7px;height:7px;border-radius:50%}
.sb-name{font-size:12px;font-weight:500;color:#374151;flex:1}
.sb-pct{font-size:11px;font-weight:600;color:#6b7280}
.sb-bar{height:5px;background:#f0f0f0;border-radius:3px;overflow:hidden}
.sb-fill{height:100%;border-radius:3px;transition:width .6s}
.sb-sub{font-size:10px;color:#9ca3af;margin-top:1px}
.weak-row{display:flex;flex-wrap:wrap;gap:8px}
.wp-tag{display:flex;align-items:center;gap:6px;padding:7px 12px;background:#fff5f5;border-radius:18px;cursor:pointer;font-size:11px;transition:background .15s}
.wp-tag:hover{background:#ffe7e5}
.wp-cat{padding:1px 5px;border-radius:5px;font-size:9px;color:white;flex-shrink:0}
.wp-name{color:#374151;font-weight:500;max-width:100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.wp-ratio{color:#ff4d4f;font-size:10px}
.guest-box{text-align:center;padding:50px 20px;background:white;border-radius:14px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.guest-icon{font-size:44px;margin-bottom:10px}
.guest-box p{font-size:15px;color:#374151;margin-bottom:2px}
.gsub{font-size:12px;color:#9ca3af;margin-bottom:18px!important}
.subj-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.sc-card{background:#f9fafb;border-radius:10px;padding:14px;border-left:3px solid var(--sc)}
.sc-top{display:flex;align-items:center;gap:6px;margin-bottom:4px}
.sc-ico{font-size:18px}.sc-name{font-size:13px;font-weight:600;color:#1f2937}
.sc-info{display:flex;gap:8px;font-size:10px;color:#9ca3af}
.side-card{background:white;border-radius:12px;padding:14px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.side-card h4{font-size:12px;font-weight:600;color:#6b7280;margin-bottom:8px}
.cal-nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.cal-arrow{cursor:pointer;font-size:12px;color:#6b7280;padding:2px 6px;border-radius:4px;user-select:none}
.cal-arrow:hover{background:#f0f4ff;color:#4f7cff}
.cal-month-label{font-size:12px;font-weight:600;color:#374151}
.cal-weekdays{display:grid;grid-template-columns:repeat(7,1fr);gap:0;margin-bottom:2px}
.cal-weekdays span{font-size:7px;color:#9ca3af;text-align:center}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:1px}
.cal-cell{aspect-ratio:1;border-radius:2px;display:flex;align-items:center;justify-content:center;font-size:7px;background:#ebedf0;color:#9ca3af}
.cal-cell.out-month{background:transparent;color:transparent}
.cal-cell.lvl1{background:#c6e48b;color:#5a8a3c}.cal-cell.lvl2{background:#7bc96f;color:#fff}.cal-cell.lvl3{background:#40a040;color:#fff}.cal-cell.lvl4{background:#216e39;color:#fff}
.cal-day{line-height:1}
.cal-legend{display:flex;align-items:center;gap:2px;font-size:7px;color:#9ca3af;margin-top:4px;justify-content:center}
.cl-dot{width:6px;height:6px;border-radius:1px}
.cl-dot.lvl0{background:#ebedf0}.cl-dot.lvl1{background:#c6e48b}.cl-dot.lvl2{background:#7bc96f}.cl-dot.lvl3{background:#40a040}.cl-dot.lvl4{background:#216e39}
.streak-display{text-align:center;padding:8px 0 4px}
.streak-num{font-size:40px;font-weight:800;color:#fa8c16;line-height:1}
.streak-unit{font-size:14px;color:#9ca3af}
.streak-sub{font-size:11px;color:#9ca3af;text-align:center}
.side-pct{display:flex;align-items:center;gap:10px}
.sp-bar-bg{flex:1;height:8px;background:#f0f0f0;border-radius:4px;overflow:hidden}
.sp-bar-fill{height:100%;background:linear-gradient(90deg,#52c41a,#4f7cff);border-radius:4px;transition:width .4s}
.sp-text{font-size:18px;font-weight:700;color:#1f2937}
.side-links{display:flex;flex-direction:column;gap:4px}
.sl-item{display:flex;align-items:center;gap:6px;padding:7px 10px;border-radius:6px;cursor:pointer;font-size:12px;color:#374151;transition:background .15s}
.sl-item:hover{background:#f0f4ff;color:#4f7cff}
.sl-item span{font-size:15px}
.lb-tabs{display:flex;gap:0;margin-bottom:8px;background:#f3f4f6;border-radius:8px;padding:2px}
.lb-tabs span{flex:1;text-align:center;padding:4px 0;font-size:11px;cursor:pointer;border-radius:6px;color:#6b7280;transition:all .15s}
.lb-tabs span.active{background:white;color:#4f7cff;font-weight:600;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.lb-list{max-height:300px;overflow-y:auto}.lb-row{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #f3f4f6;font-size:12px}
.lb-idx{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;background:#f3f4f6;flex-shrink:0}
.lb-idx.r0{background:#fbbf24;color:white}.lb-idx.r1{background:#9ca3af;color:white}.lb-idx.r2{background:#d97706;color:white}
.lb-name{flex:1;color:#374151;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.lb-val{color:#6b7280;font-weight:600;flex-shrink:0}
.lb-empty{text-align:center;padding:16px;color:#9ca3af;font-size:12px}
.cal-footer{text-align:center;font-size:11px;color:#9ca3af;margin-top:8px;padding-top:8px;border-top:1px solid #f0f0f0}
@media(max-width:768px){.main-layout{grid-template-columns:1fr}.two-col{grid-template-columns:1fr}.subj-cards{grid-template-columns:repeat(2,1fr)}.hero h1{font-size:22px}.hero{padding:16px}.home-page{padding:0 12px}}
</style>