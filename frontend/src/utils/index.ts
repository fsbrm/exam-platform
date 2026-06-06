export function formatDate(date: string | Date): string {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

export function formatDateTime(date: string | Date): string {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleString('zh-CN')
}

export function getTypeLabel(type: string): string {
  const map: Record<string, string> = { SINGLE: '单选题', MULTI: '多选题', JUDGE: '判断题', FILL: '填空题' }
  return map[type] || type
}

export function getDifficultyLabel(difficulty: string): string {
  const map: Record<string, string> = { EASY: '简单', MEDIUM: '中等', HARD: '困难' }
  return map[difficulty] || difficulty
}

export function getDifficultyColor(difficulty: string): string {
  const map: Record<string, string> = { EASY: 'success', MEDIUM: 'warning', HARD: 'danger' }
  return map[difficulty] || 'info'
}
