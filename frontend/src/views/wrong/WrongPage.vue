<template>
  <div class="wrong-page">
    <div class="wp-header">
      <h2>📝 错题本</h2>
      <span class="wp-stats">共 {{ totalCount }} 题 |
        <span class="tag-dk">不会 {{ stats.dontknow }}</span>
        <span class="tag-cr">粗心 {{ stats.careless }}</span>
        <span class="tag-uf">不熟 {{ stats.unfamiliar }}</span>
        <span class="tag-fv">⭐ 收藏 {{ stats.favorite }}</span>
      </span>
    </div>

    <div class="wp-body">
      <!-- Left Tabs -->
      <aside class="wp-tabs">
        <div class="wp-tab" :class="{ active: activeTab === 'all' }" @click="switchTab('all')">
          <span>全部</span><span class="wp-tab-num">{{ totalCount }}</span>
        </div>
        <div class="wp-tab" :class="{ active: activeTab === 'dontknow' }" @click="switchTab('dontknow')">
          <span>😵 不会</span><span class="wp-tab-num">{{ stats.dontknow }}</span>
        </div>
        <div class="wp-tab" :class="{ active: activeTab === 'careless' }" @click="switchTab('careless')">
          <span>😅 粗心</span><span class="wp-tab-num">{{ stats.careless }}</span>
        </div>
        <div class="wp-tab" :class="{ active: activeTab === 'unfamiliar' }" @click="switchTab('unfamiliar')">
          <span>🤔 不熟</span><span class="wp-tab-num">{{ stats.unfamiliar }}</span>
        </div>
        <div class="wp-tab-divider"></div>
        <div class="wp-tab" :class="{ active: activeTab === 'favorite' }" @click="switchTab('favorite')">
          <span>⭐ 收藏</span><span class="wp-tab-num">{{ stats.favorite }}</span>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="wp-main">
        <!-- Filter Bar -->
        <div class="wp-filters">
          <div class="wp-filter-group">
            <el-select v-model="filterSubjectId" placeholder="科目" clearable size="small" @change="onSubjectChange">
              <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" />
            </el-select>
            <el-select v-model="filterChapterId" placeholder="章节" clearable size="small" :disabled="!filterSubjectId">
              <el-option v-for="c in chapters" :key="c.id" :label="c.name" :value="c.id" />
            </el-select>
          </div>
          <div class="wp-filter-group">
            <el-select v-model="filterMonth" placeholder="月份" clearable size="small" @change="loadData">
              <el-option v-for="m in months" :key="m.value" :label="m.label" :value="m.value" />
            </el-select>
          </div>
          <el-button size="small" type="primary" :disabled="questions.length === 0" @click="startRedo">重做筛选结果</el-button>
        </div>

        <el-empty v-if="questions.length === 0" description="太棒了，这里没有错题！" />

        <!-- Question Cards grouped by date -->
        <div v-else class="wp-list">
          <template v-for="group in groupedQuestions" :key="group.date">
            <div class="wp-date-header">{{ group.date }}</div>
            <div v-for="q in group.items" :key="q.question_id" class="wp-card" @click="goPractice(q)">
              <div class="wpc-top">
                <span class="wpc-subject">{{ subjectIcon(q.subject_name) }} {{ q.subject_name }}</span>
                <span class="wpc-arrow">›</span>
                <span class="wpc-chapter">{{ q.chapter_name }}</span>
                <span v-if="q.mastery" class="wpc-mastery" :class="'m-'+q.mastery">
                  {{ masteryLabel(q.mastery) }}
                </span>
                <span v-if="q.is_favorited == 1" class="wpc-fav">⭐</span>
                <span class="wpc-count">错{{ q.wrong_count }}次</span>
              </div>
              <div class="wpc-content" v-html="truncateHtml(q.content, 120)"></div>
            </div>
          </template>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()

const activeTab = ref('all')
const questions = ref<any[]>([])
const filterSubjectId = ref<number | null>(null)
const filterChapterId = ref<number | null>(null)
const filterMonth = ref<string | null>(null)

const subjects = ref<any[]>([])
const chapters = ref<any[]>([])

// Stats
const stats = reactive({ total: 0, dontknow: 0, careless: 0, unfamiliar: 0, favorite: 0 })
const totalCount = computed(() => stats.total)

const months = computed(() => {
  const now = new Date()
  const list: { label: string; value: string }[] = []
  for (let i = 0; i < 12; i++) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1)
    const value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
    list.push({ label: value, value })
  }
  return list
})

const groupedQuestions = computed(() => {
  const groups: Record<string, any[]> = {}
  for (const q of questions.value) {
    const d = q.last_wrong_at ? new Date(q.last_wrong_at).toLocaleDateString('zh-CN') : '未知'
    if (!groups[d]) groups[d] = []
    groups[d].push(q)
  }
  return Object.entries(groups).map(([date, items]) => ({ date, items }))
})

function switchTab(tab: string) {
  activeTab.value = tab
  loadData()
}

function onSubjectChange() {
  filterChapterId.value = null
  loadChapters()
  loadData()
}

async function loadChapters() {
  if (!filterSubjectId.value) { chapters.value = []; return }
  try {
    const tr: any = await api.get('/knowledge/tree', { params: { subjectId: filterSubjectId.value } })
    if (tr.code === 200 && tr.data.tree) {
      const subj = tr.data.tree.find((s: any) => s.id === filterSubjectId.value)
      chapters.value = subj?.chapters || []
    }
  } catch { chapters.value = [] }
}

async function loadData() {
  const params: any = {}
  if (activeTab.value === 'favorite') params.favoriteOnly = true
  else if (activeTab.value !== 'all') params.mastery = activeTab.value
  if (filterSubjectId.value) params.subjectId = filterSubjectId.value
  if (filterChapterId.value) params.chapterId = filterChapterId.value
  if (filterMonth.value) params.yearMonth = filterMonth.value

  try {
    const res: any = await api.get('/wrong/enhanced', { params })
    if (res.code === 200) {
      questions.value = res.data.questions || []

      // Load all stats in parallel
      const [allRes, dkRes, crRes, ufRes, fvRes] = await Promise.allSettled([
        api.get('/wrong/enhanced'),
        api.get('/wrong/enhanced', { params: { mastery: 'dontknow' } }),
        api.get('/wrong/enhanced', { params: { mastery: 'careless' } }),
        api.get('/wrong/enhanced', { params: { mastery: 'unfamiliar' } }),
        api.get('/wrong/enhanced', { params: { favoriteOnly: true } }),
      ])
      stats.total = allRes.status === 'fulfilled' ? (allRes.value as any)?.data?.total || 0 : 0
      stats.dontknow = dkRes.status === 'fulfilled' ? (dkRes.value as any)?.data?.total || 0 : 0
      stats.careless = crRes.status === 'fulfilled' ? (crRes.value as any)?.data?.total || 0 : 0
      stats.unfamiliar = ufRes.status === 'fulfilled' ? (ufRes.value as any)?.data?.total || 0 : 0
      stats.favorite = fvRes.status === 'fulfilled' ? (fvRes.value as any)?.data?.total || 0 : 0
    }
  } catch {}
}

function startRedo() {
  router.push('/practice?wrong=true')
}

function goPractice(q: any) {
  router.push(`/practice?questionId=${q.question_id}&from=wrong`)
}

function masteryLabel(m: string) {
  const map: Record<string, string> = { dontknow: '😵 不会', careless: '😅 粗心', unfamiliar: '🤔 不熟' }
  return map[m] || m
}

function subjectIcon(name: string) {
  const map: Record<string, string> = {
    '数据结构': '🌲', '计算机组成原理': '💻', '操作系统': '⚙️', '计算机网络': '🌐',
  }
  return map[name] || '📚'
}

function truncateHtml(html: string, maxLen: number) {
  if (!html) return ''
  const text = html.replace(/<[^>]*>/g, '').trim()
  return text.length > maxLen ? text.substring(0, maxLen) + '...' : text
}

onMounted(async () => {
  try {
    const subRes: any = await api.get('/subjects')
    if (subRes.code === 200) subjects.value = subRes.data || []
  } catch {}
  loadData()
})
</script>

<style scoped>
.wrong-page { max-width: 1200px; margin: 0 auto; padding: 20px; }
.wp-header { display: flex; align-items: baseline; gap: 16px; margin-bottom: 20px; }
.wp-header h2 { margin: 0; font-size: 22px; }
.wp-stats { font-size: 13px; color: #6b7280; }
.wp-stats .tag-dk { color: #ef4444; }
.wp-stats .tag-cr { color: #f59e0b; }
.wp-stats .tag-uf { color: #8b5cf6; }
.wp-stats .tag-fv { color: #eab308; }

.wp-body { display: flex; gap: 20px; }
.wp-tabs {
  width: 140px; flex-shrink: 0; display: flex; flex-direction: column; gap: 2px;
  background: white; border-radius: 12px; padding: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  height: fit-content; position: sticky; top: 80px;
}
.wp-tab {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 13px;
  color: #374151; transition: all 0.15s;
}
.wp-tab:hover { background: #f3f4f6; }
.wp-tab.active { background: #eef2ff; color: #4f7cff; font-weight: 600; }
.wp-tab-num { font-size: 11px; color: #9ca3af; background: #f3f4f6; padding: 1px 7px; border-radius: 10px; }
.wp-tab.active .wp-tab-num { background: #dbeafe; color: #4f7cff; }
.wp-tab-divider { height: 1px; background: #e5e7eb; margin: 4px 8px; }

.wp-main { flex: 1; min-width: 0; }
.wp-filters { display: flex; gap: 10px; align-items: center; margin-bottom: 16px; flex-wrap: wrap; }
.wp-filter-group { display: flex; gap: 8px; }

.wp-list { display: flex; flex-direction: column; gap: 8px; }
.wp-date-header {
  font-size: 12px; font-weight: 600; color: #9ca3af; padding: 8px 0 4px;
  border-bottom: 1px solid #f0f0f0; margin-top: 8px;
}
.wp-card {
  background: white; border-radius: 10px; padding: 14px 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04); cursor: pointer;
  transition: box-shadow 0.15s;
}
.wp-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }

.wpc-top { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.wpc-subject { font-size: 12px; color: #6b7280; font-weight: 500; }
.wpc-arrow { color: #d1d5db; font-size: 12px; }
.wpc-chapter { font-size: 12px; color: #9ca3af; }
.wpc-mastery { font-size: 11px; padding: 1px 8px; border-radius: 8px; font-weight: 500; }
.m-dontknow { background: #fef2f2; color: #ef4444; }
.m-careless { background: #fffbeb; color: #f59e0b; }
.m-unfamiliar { background: #f5f3ff; color: #8b5cf6; }
.wpc-fav { font-size: 12px; }
.wpc-count { font-size: 11px; color: #ef4444; background: #fef2f2; padding: 1px 6px; border-radius: 6px; margin-left: auto; }

.wpc-content { font-size: 13px; color: #4b5563; line-height: 1.5; }
</style>
