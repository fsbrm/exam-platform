import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory('/exam-platform/'),
  routes: [
    { path: '/', name: 'home', component: () => import('@/views/home/HomePage.vue') },
    { path: '/login', name: 'login', component: () => import('@/views/auth/LoginPage.vue') },
    { path: '/register', name: 'register', component: () => import('@/views/auth/RegisterPage.vue') },
    { path: '/papers', name: 'papers', component: () => import('@/views/papers/PapersPage.vue') },
    { path: '/knowledge', name: 'knowledge', component: () => import('@/views/knowledge/KnowledgeGraph.vue') },
    { path: '/practice', name: 'practice', component: () => import('@/views/practice/PracticePage.vue') },
    { path: '/exam', name: 'exam', component: () => import('@/views/exam/ExamPage.vue') },
    { path: '/exam/result/:id', name: 'examResult', component: () => import('@/views/exam/ExamResult.vue') },
    { path: '/wrong', name: 'wrong', component: () => import('@/views/wrong/WrongPage.vue') },
    { path: '/analytics', name: 'analytics', component: () => import('@/views/analytics/AnalyticsPage.vue') },
    { path: '/profile', name: 'profile', component: () => import('@/views/profile/ProfilePage.vue') },
    { path: '/ai', name: 'ai', component: () => import('@/views/ai/AiChatPage.vue') },
    { path: '/admin', name: 'admin', component: () => import('@/views/admin/AdminPage.vue'), meta: { requireAdmin: true } },
    { path: '/admin/questions', name: 'adminQuestions', component: () => import('@/views/admin/QuestionManage.vue'), meta: { requireAdmin: true } },
    { path: '/admin/users', name: 'adminUsers', component: () => import('@/views/admin/UserManage.vue'), meta: { requireAdmin: true } },
    { path: '/subject/:id', redirect: '/papers' },
    { path: '/paper/:paperId', name: 'paperDetail', component: () => import('@/views/paper/PaperDetailPage.vue') },
    { path: '/question/:questionId', name: 'questionView', component: () => import('@/views/paper/QuestionViewPage.vue') },
  ]
})

router.beforeEach((to, _from, next) => {
  const publicPages = ['/', '/login', '/register', '/papers', '/knowledge']
  const publicPrefixes = ['/paper', '/question']
  const token = localStorage.getItem('token')

  // Not logged in
  if (!token && !publicPages.includes(to.path) && !publicPrefixes.some((p: string) => to.path.startsWith(p))) {
    next('/login')
    return
  }

  // Admin route guard
  if (to.meta.requireAdmin) {
    const savedUser = localStorage.getItem('user')
    const user = savedUser ? JSON.parse(savedUser) : null
    if (!user || user.role !== 'ADMIN') {
      next('/')
      return
    }
  }

  next()
})

export default router