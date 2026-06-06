<template>
  <div class="page-container ai-page">
    <h2 class="page-title">🤖 AI 学习助手</h2>

    <div class="ai-layout">
      <!-- Chat Area -->
      <div class="chat-area card">
        <div class="chat-messages" ref="chatRef">
          <div v-if="messages.length === 0" class="chat-empty">
            <p>👋 你好！我是你的AI学习助手</p>
            <p class="sub">有不懂的题目或知识点，随时问我！</p>
            <div class="quick-prompts">
              <el-tag v-for="p in quickPrompts" :key="p" @click="sendQuick(p)" class="prompt-tag">{{ p }}</el-tag>
            </div>
          </div>
          <div v-for="(msg, i) in messages" :key="i" class="chat-msg" :class="msg.role">
            <div class="msg-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
            <div class="msg-content" v-html="formatMsg(msg.content)"></div>
          </div>
          <div v-if="typing" class="chat-msg assistant">
            <div class="msg-avatar">🤖</div>
            <div class="msg-content typing-dots"><span>.</span><span>.</span><span>.</span></div>
          </div>
        </div>

        <div class="chat-input">
          <el-input
            v-model="inputText"
            placeholder="输入你的问题..."
            @keydown.enter="sendMessage"
            size="large"
            :disabled="typing"
          >
            <template #append>
              <el-button :icon="Promotion" @click="sendMessage" :loading="typing" />
            </template>
          </el-input>
        </div>
      </div>

      <!-- Side Panel -->
      <div class="side-panel card">
        <h3>快捷功能</h3>
        <el-button type="primary" style="width:100%;margin-bottom:12px" @click="analyzeWeakPoints">
          📊 分析我的薄弱点
        </el-button>
        <el-select v-model="analyzeSubject" placeholder="选择科目" style="width:100%;margin-bottom:12px">
          <el-option label="408 计算机综合" :value="1" />
          <el-option label="高等数学" :value="2" />
        </el-select>

        <el-divider />
        <h4>使用技巧</h4>
        <ul class="tips-list">
          <li>粘贴题目内容，AI帮你分步解答</li>
          <li>询问知识点概念和考点</li>
          <li>让AI分析你的薄弱环节</li>
          <li>适合408计算机和高等数学</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const messages = ref<any[]>([])
const inputText = ref('')
const typing = ref(false)
const analyzeSubject = ref(1)
const chatRef = ref()

const quickPrompts = [
  '帮我解释二叉树的遍历方式',
  '微分中值定理包括哪些？',
  '如何比较不同排序算法的时间复杂度？',
  '什么是虚拟内存？'
]

onMounted(() => {
  const question = route.query.question as string
  if (question) {
    inputText.value = `请帮我讲解这道题：${decodeURIComponent(question)}`
    sendMessage()
  }
})

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || typing.value) return

  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  typing.value = true

  await nextTick()
  scrollToBottom()

  try {
    const res: any = await api.post('/ai/chat', { question: text, context: '' })
    if (res.code === 200) {
      messages.value.push({ role: 'assistant', content: res.data.response })
    }
  } catch {
    messages.value.push({ role: 'assistant', content: '抱歉，AI服务暂时不可用，请检查API配置。' })
  } finally {
    typing.value = false
    await nextTick()
    scrollToBottom()
  }
}

function sendQuick(text: string) {
  inputText.value = text
  sendMessage()
}

async function analyzeWeakPoints() {
  ElMessage.info('正在分析你的薄弱环节...')
  try {
    const res: any = await api.get(`/ai/analyze/${analyzeSubject.value}`)
    if (res.code === 200) {
      messages.value.push({ role: 'assistant', content: res.data.response })
      await nextTick()
      scrollToBottom()
    }
  } catch {}
}

function formatMsg(content: string) {
  return content.replace(/\n/g, '<br>').replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
}

function scrollToBottom() {
  if (chatRef.value) chatRef.value.scrollTop = chatRef.value.scrollHeight
}
</script>

<style scoped>
.ai-page { max-width: 1100px; }
.ai-layout { display: grid; grid-template-columns: 1fr 280px; gap: 20px; }

.chat-area { display: flex; flex-direction: column; height: calc(100vh - 180px); }
.chat-messages { flex: 1; overflow-y: auto; padding: 20px; }

.chat-empty { text-align: center; padding: 60px 20px; }
.chat-empty p { font-size: 18px; }
.chat-empty .sub { font-size: 14px; color: var(--text-secondary); margin-top: 8px; }

.quick-prompts { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 24px; }
.prompt-tag { cursor: pointer; }

.chat-msg { display: flex; gap: 12px; margin-bottom: 20px; }
.chat-msg.user { flex-direction: row-reverse; }
.chat-msg.user .msg-content { background: var(--primary-color); color: white; border-radius: 16px 4px 16px 16px; }
.chat-msg.assistant .msg-content { background: var(--bg-color); border-radius: 4px 16px 16px 16px; }

.msg-avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; background: var(--card-bg); }
.msg-content { padding: 12px 16px; font-size: 14px; line-height: 1.7; max-width: 80%; }

.typing-dots span { display: inline-block; animation: blink 1.4s infinite; font-size: 20px; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%, 60%, 100% { opacity: 0.2; } 30% { opacity: 1; } }

.chat-input { padding: 16px 20px; border-top: 1px solid var(--border-color); }

.side-panel { padding: 20px; height: fit-content; }
.side-panel h3 { margin-bottom: 16px; }
.tips-list { padding-left: 18px; }
.tips-list li { font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; line-height: 1.5; }

@media (max-width: 768px) {
  .ai-layout { grid-template-columns: 1fr; }
  .side-panel { display: none; }
}
</style>
