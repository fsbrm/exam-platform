<template>
  <div class="paper-detail">
    <div class="pd-topbar">
      <div class="pd-back" @click="$router.back()"><span>&larr;</span> 返回总览</div>
      <div class="pd-title"><h2>{{ paperInfo.year }}年408计算机基础综合真题</h2><span class="pd-total">{{ questions.length }}道题目</span></div>
      <div class="pd-progress" v-if="questions.length > 0">已完成 {{ answeredCount }} / {{ questions.length }}</div>
      <div class="ph-settings-wrap" style="position:relative">
        <button class="ph-settings-btn" @click.stop="showSettings=!showSettings" title="设置"><el-icon :size="18"><Setting /></el-icon></button>
        <div class="ph-settings-drop" v-if="showSettings" @click.stop>
          <div class="psd-item"><span>做题反馈</span><el-switch v-model="feedbackOn" size="small" /></div>
          <div class="psd-item"><span>键盘快捷键</span><el-switch v-model="keyboardOn" size="small" /></div>
          <div class="psd-item"><span>连击计数</span><el-switch v-model="comboOn" size="small" /></div>
          <div class="psd-item"><span>自动提交</span><el-switch v-model="autoSubmitOn" size="small" /></div>
        </div>
      </div>
    </div>

    <div class="pd-body" v-if="questions.length > 0">
      <nav class="pd-nav">
        <div class="pd-nav-header">题号导航</div>
        <div class="pd-nav-grid">
          <div v-for="(q, idx) in questions" :key="q.id || q.questionNumber" class="pd-nav-num"
            :class="{ active: currentIndex===idx, correct: q.userCorrect===true, wrong: q.userCorrect===false, done: q.userAnswer,
              'm-mastered': q._mastery==='mastered', 'm-unfamiliar': q._mastery==='unfamiliar', 'm-dontknow': q._mastery==='dontknow', 'm-careless': q._mastery==='careless' }"
            @click="jumpTo(idx)">{{ q.questionNumber || q.question_number }}</div>
        </div>
        <div class="pd-legend"><span><i class="pd-ld active"></i>当前</span><span><i class="pd-ld done"></i>已答</span><span><i class="pd-ld correct"></i>正确</span><span><i class="pd-ld wrong"></i>错误</span></div>
      </nav>

      <main class="pd-main">
        <div class="pd-question-card" v-if="currentQuestion">
          <div class="pd-q-header">
            <span class="pd-q-num">第 {{ currentQuestion.questionNumber || currentQuestion.question_number }} 题</span>
            <el-tag :type="diffTagType" size="small">{{ diffLabel }}</el-tag>
            <el-tag :type="typeTagType" size="small" effect="plain">{{ typeLabel }}</el-tag>
            <span class="pd-q-year">{{ paperInfo.year }}年真题</span>
            <div class="mastery-btns">
              <el-button :type="currentMastery==='mastered'?'success':''" size="small" plain @click="markMastery('mastered')">掌握</el-button>
              <el-button :type="currentMastery==='unfamiliar'?'warning':''" size="small" plain @click="markMastery('unfamiliar')">不熟</el-button>
              <el-button :type="currentMastery==='dontknow'?'danger':''" size="small" plain @click="markMastery('dontknow')">不会</el-button>
              <el-button size="small" plain @click="markMastery('careless')" :style="currentMastery==='careless'?{color:'#7c3aed',borderColor:'#7c3aed',background:'#f5f3ff'}:{}">粗心</el-button>
            </div>
          </div>
          <div class="pd-q-content"><div v-if="currentQuestion.image"><img :src="currentQuestion.image" style="max-width:100%;border-radius:8px;margin-bottom:12px"/></div><div v-html="currentQuestion.content"></div></div>
          <div class="pd-options" v-if="parsedOptions.length>0 && !isComprehensive">
            <div v-for="opt in parsedOptions" :key="opt.key" class="pd-option"
              :class="{ selected: selectedAnswer===opt.key && !showResult, correct: showResult && opt.key===currentQuestion.answer, wrong: showResult && selectedAnswer===opt.key && opt.key!==currentQuestion.answer }"
              @click="selectOption(opt.key)">
              <span class="pd-opt-key">{{ opt.key }}</span><span class="pd-opt-val"><span v-html="opt.value"></span></span>
              <span class="pd-opt-icon" v-if="showResult && opt.key===currentQuestion.answer">&#10003;</span>
              <span class="pd-opt-icon err" v-if="showResult && selectedAnswer===opt.key && opt.key!==currentQuestion.answer">&#10007;</span>
            </div>
          </div>
          <div v-if="isComprehensive" class="pd-result ok"><div class="pd-result-header">📝 参考答案</div><div v-html="currentQuestion.answer"></div><div v-if="currentQuestion.analysis" style="margin-top:12px"><strong>解析：</strong>{{ currentQuestion.analysis }}</div></div>
          <div v-if="showResult" class="pd-result" :class="{ok:lastCorrect,err:!lastCorrect}">
            <div class="pd-result-header">{{ lastCorrect?'✅ 回答正确':'❌ 回答错误' }}<span v-if="!lastCorrect">，正确答案：{{ currentQuestion.answer }}</span></div>
            <div class="pd-result-analysis" v-if="currentQuestion.analysis"><strong>解析：</strong>{{ currentQuestion.analysis }}</div>
          </div>
          <div class="pd-actions">
            <el-button v-if="!showResult && selectedAnswer && !isComprehensive" type="primary" size="large" @click="submitAnswer">提交答案</el-button>
            <div class="pd-nav-btns">
              <el-button :disabled="currentIndex===0" @click="prevQuestion" size="large">上一题</el-button>
              <span class="pd-nav-info">{{ currentIndex+1 }}/{{ questions.length }}</span>
              <el-button :disabled="currentIndex>=questions.length-1" @click="nextQuestion" size="large">下一题</el-button>
            </div>
          </div>
        </div>
        <div v-else class="pd-empty">请从左侧题号开始答题</div>
      </main>

      <aside class="pd-summary"><h4>答题卡</h4>
        <div class="pd-summary-grid">
          <div v-for="(q2,idx2) in questions" :key="'s'+q2.id" class="pd-s-cell"
            :class="{ done:q2.userAnswer, correct:q2.userCorrect===true, wrong:q2.userCorrect===false, 'm-mastered':q2._mastery==='mastered', 'm-unfamiliar':q2._mastery==='unfamiliar', 'm-dontknow':q2._mastery==='dontknow', 'm-careless':q2._mastery==='careless' }">
            {{ q2.questionNumber || q2.question_number }}</div>
        </div>
      </aside>
    </div>

    <div v-else-if="loading" class="pd-loading"><p>加载题目中...</p></div>
    <div v-else class="pd-empty-state"><el-empty description="该年份暂无题目数据"/><el-button @click="$router.back()">返回</el-button></div>

    <!-- Feedback & Combo floats -->
    <div v-if="comboOn && comboCount>1" class="pp-combo-badge">{{ comboCount }}连</div>
    <div v-if="comboOn && showCombo" class="pp-float-combo">{{ comboTxt }}</div>
    <div v-if="keyboardOn" class="pp-kb-hint"><span>1-4 选项</span><span>空格 提交</span><span>←→ 切题</span><span>Q/W/E/R 掌握</span><span>C 收藏</span><span>Z 重做</span></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import { Setting } from '@element-plus/icons-vue'

const route = useRoute()
const loading = ref(true)
const questions = ref<any[]>([])
const currentIndex = ref(0)
const selectedAnswer = ref('')
const showResult = ref(false)
const lastCorrect = ref(false)
const answeredCount = ref(0)
const currentMastery = ref('')

const paperInfo = reactive({ year: 0, name: '' })
const showSettings = ref(false)

// Settings (inline, no localStorage needed for paper page)
const feedbackOn = ref(false)
const keyboardOn = ref(false)
const comboOn = ref(false)
const autoSubmitOn = ref(false)

// Combo
const comboCount = ref(0)
const showCombo = ref(false)
const comboTxt = ref('')

const currentQuestion = computed(() => questions.value[currentIndex.value] || null)
const parsedOptions = computed(() => {
  if (!currentQuestion.value) return []
  try { const opts = typeof currentQuestion.value.options==='string'?JSON.parse(currentQuestion.value.options):currentQuestion.value.options; if (Array.isArray(opts)) return opts; if (opts && typeof opts==='object') return Object.entries(opts).map(([k,v])=>({key:k,value:v})); return [] } catch { return [] }
})
const typeLabel = computed(()=>({SINGLE:'单选',MULTI:'多选',COMPREHENSIVE:'综合'})[currentQuestion.value?.type]||'')
const typeTagType = computed(()=>({SINGLE:'',MULTI:'warning',COMPREHENSIVE:'danger'})[currentQuestion.value?.type]||'')
const diffTagType = computed(()=>({EASY:'success',MEDIUM:'warning',HARD:'danger'})[currentQuestion.value?.difficulty]||'info')
const diffLabel = computed(()=>({EASY:'简单',MEDIUM:'中等',HARD:'困难'})[currentQuestion.value?.difficulty]||'')
const isComprehensive = computed(()=>currentQuestion.value?.type==='COMPREHENSIVE')

function selectOption(key:string){if(showResult.value)return;selectedAnswer.value=key;if(autoSubmitOn.value&&currentQuestion.value?.type!=='MULTI')submitAnswer()}
function jumpTo(idx:number){currentIndex.value=idx;resetState()}
async function submitAnswer(){
  if(!currentQuestion.value||!selectedAnswer.value)return
  try{const res:any=await api.post('/practice/submit',{questionId:currentQuestion.value.id,answer:selectedAnswer.value})
  if(res.code===200){lastCorrect.value=res.data.isCorrect;showResult.value=true;const q=questions.value[currentIndex.value];q.userAnswer=selectedAnswer.value;q.userCorrect=res.data.isCorrect;answeredCount.value=questions.value.filter((x:any)=>x.userAnswer).length
  q._mastery=res.data.isCorrect?'mastered':'dontknow';currentMastery.value=q._mastery;markMasteryApi(q.id,q._mastery)
  showFeedback(res.data.isCorrect);triggerCombo(res.data.isCorrect)}}catch{}}
function prevQuestion(){if(currentIndex.value>0){currentIndex.value--;resetState()}}
function nextQuestion(){if(currentIndex.value<questions.value.length-1){currentIndex.value++;resetState()}}
function resetState(){selectedAnswer.value='';showResult.value=false;const q=questions.value[currentIndex.value];if(q)currentMastery.value=q._mastery||''}
async function markMastery(level:string){if(!currentQuestion.value)return;try{await markMasteryApi(currentQuestion.value.id,level);const q=questions.value[currentIndex.value];q._mastery=level;currentMastery.value=level}catch{}}
async function markMasteryApi(qid:number,level:string){try{await api.post('/user/mastery/'+qid,{mastery:level})}catch{}}

// Keyboard
function onKeyDown(e:KeyboardEvent){if(!keyboardOn.value||!currentQuestion.value)return;const q=currentQuestion.value
  if(e.key>='1'&&e.key<='9'&&!showResult.value&&['SINGLE','MULTI'].includes(q.type)){const idx=parseInt(e.key)-1;const opts=parsedOptions.value;if(idx<opts.length)selectOption(opts[idx].key)}
  if((e.key===' '||e.key==='Enter')&&!showResult.value&&selectedAnswer.value){e.preventDefault();submitAnswer()}
  if(e.key==='ArrowLeft'&&currentIndex.value>0)prevQuestion();if(e.key==='ArrowRight'&&currentIndex.value<questions.value.length-1)nextQuestion()
  if(e.key==='q'||e.key==='Q')markMastery('mastered');if(e.key==='w'||e.key==='W')markMastery('unfamiliar');if(e.key==='e'||e.key==='E')markMastery('dontknow');if(e.key==='r'||e.key==='R')markMastery('careless')
  if(e.key==='z'||e.key==='Z'){selectedAnswer.value='';showResult.value=false}}

// Feedback
function showFeedback(isCorrect:boolean){if(!feedbackOn.value)return;const main=isCorrect?'Niceeee~~~ 🎉':'我真受不了嘞！ 😤';const extras=isCorrect?['太棒了！✨','真厉害！🔥','稳准狠！💯']:['又错了... 💔','再想想！🤔','差一点！😭'];const rareBonus=isCorrect&&Math.random()<0.5?"Let's gou ! ! ! 🚀":null;const godBonus=isCorrect&&Math.random()<0.4?'都是同龄人，我原本没想降维打击！！！ 👽':null;const nameBonus=isCorrect&&Math.random()<0.2?'流水的天才，铁打的大佬 ！ 👑':null;let all=[main,...extras];if(rareBonus)all.splice(1,0,rareBonus);if(godBonus)all.splice(1,0,godBonus);if(nameBonus)all.splice(1,0,nameBonus);const count=1+Math.floor(Math.random()*Math.min(all.length-1,3));all=all.slice(0,count);for(let i=0;i<all.length;i++){const el=document.createElement('div');el.className='feedback-float '+(isCorrect?'fb-correct':'fb-wrong');el.textContent=all[i];el.style.animationDuration=(4+Math.random()*3)+'s';el.style.top=(25+Math.random()*35)+'%';el.style.animationDelay=(i*0.3)+'s';document.body.appendChild(el);setTimeout(()=>el.remove(),8000)}}
function triggerCombo(isCorrect:boolean){if(!comboOn.value)return;if(isCorrect){comboCount.value++;if(comboCount.value===3)flashCombo('春风若有怜花意，可否许我再少年 🌸');else if(comboCount.value===5)flashCombo('须知少日拏云志，曾许人间第一流 ⛰️');else if(comboCount.value===8)flashCombo('仰天大笑出门去，我辈岂是蓬蒿人 🎋');else if(comboCount.value===12)flashCombo('长风破浪会有时，直挂云帆济沧海 ⛵');else if(comboCount.value===18)flashCombo('大鹏一日同风起，扶摇直上九万里 🦅');else if(comboCount.value===25)flashCombo('会当凌绝顶，一览众山小 🏔️');else if(comboCount.value===30)flashCombo('杀~杀~杀~！ ⚔️')}else{comboCount.value=0}}
function flashCombo(txt:string){comboTxt.value=txt;showCombo.value=true;setTimeout(()=>{showCombo.value=false},2500)}

onMounted(async()=>{
  window.addEventListener('keydown',onKeyDown)
  document.addEventListener('click',()=>showSettings.value=false)
  const paperId=route.params.paperId||route.query.paperId
  try{const res:any=await api.get(`/papers/${paperId}/questions`)
  if(res.code===200){const list=res.data||[];questions.value=list.map((q:any)=>({...q,questionNumber:q.question_number||q.questionNumber,userAnswer:null,userCorrect:null,_mastery:''}))}
  const pres:any=await api.get('/papers?subjectId=1');if(pres.code===200){const paper=(pres.data||[]).find((p:any)=>p.id===Number(paperId));if(paper){paperInfo.year=paper.year;paperInfo.name=paper.name}}
  // Load mastery
  try{const mr:any=await api.get('/user/mastery');if(mr.code===200&&mr.data){for(const q of questions.value){if(mr.data[q.id])q._mastery=mr.data[q.id]}}}catch{}}catch(e){console.error(e)}finally{loading.value=false}})
onUnmounted(()=>{window.removeEventListener('keydown',onKeyDown)})
</script>

<style scoped>
.paper-detail{min-height:100vh;background:#f5f7fa;display:flex;flex-direction:column}
.pd-topbar{background:white;border-bottom:1px solid #e5e7eb;padding:12px 24px;display:flex;align-items:center;gap:24px;position:sticky;top:56px;z-index:100}
.pd-back{cursor:pointer;color:#4f7cff;font-size:14px;font-weight:500}.pd-back:hover{opacity:.8}
.pd-title h2{font-size:18px;margin:0;display:inline}.pd-total{font-size:13px;color:#9ca3af;margin-left:10px}
.pd-progress{margin-left:auto;font-size:14px;color:#6b7280}
.pd-body{display:flex;flex:1;overflow:hidden}
.pd-nav{width:180px;background:white;border-right:1px solid #e5e7eb;padding:16px;overflow-y:auto;flex-shrink:0}
.pd-nav-header{font-size:13px;font-weight:600;color:#6b7280;margin-bottom:12px}
.pd-nav-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}
.pd-nav-num{width:28px;height:28px;display:flex;align-items:center;justify-content:center;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;background:#f3f4f6;color:#6b7280;transition:all .15s}
.pd-nav-num:hover{background:#e0e7ff;color:#4f7cff}.pd-nav-num.active{background:#4f7cff;color:white}
.pd-nav-num.correct{background:#c8e6c9;color:#2e7d32}.pd-nav-num.wrong{background:#ffd6d6;color:#c62828}.pd-nav-num.done{background:#dbeafe;color:#4f7cff}
.pd-nav-num.m-mastered{background:#c8e6c9;color:#2e7d32}.pd-nav-num.m-unfamiliar{background:#fff3e0;color:#e65100}.pd-nav-num.m-dontknow{background:#fce4ec;color:#c62828}.pd-nav-num.m-careless{background:#ede9fe;color:#6a1b9a}
.pd-main{flex:1;overflow-y:auto;padding:24px}.pd-question-card{max-width:800px;margin:0 auto}
.pd-q-header{display:flex;align-items:center;gap:10px;margin-bottom:20px;flex-wrap:wrap}
.pd-q-num{font-size:20px;font-weight:700;color:#1f2937}.pd-q-year{margin-left:auto;font-size:12px;color:#9ca3af}
.pd-q-content{font-size:16px;line-height:2.2;padding:24px;background:white;color:#1f2937;border-radius:12px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.pd-q-content :deep(img){max-width:100%;height:auto;border-radius:8px;margin:8px 0}
.pd-options{display:flex;flex-direction:column;gap:10px;margin-bottom:20px}
.pd-option{display:flex;align-items:center;gap:12px;padding:14px 18px;background:white;border:2px solid #e5e7eb;border-radius:10px;cursor:pointer;transition:all .2s}
.pd-option:hover:not(.correct):not(.wrong){border-color:#93c5fd;background:#eff6ff}
.pd-option.selected{border-color:#4f7cff;background:#eff6ff}.pd-option.correct{border-color:#52c41a;background:#f6ffed}.pd-option.wrong{border-color:#ff4d4f;background:#fff2f0}
.pd-opt-key{width:34px;height:34px;border-radius:50%;background:#f3f4f6;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;flex-shrink:0}
.pd-option.correct .pd-opt-key{background:#52c41a;color:white}.pd-option.wrong .pd-opt-key{background:#ff4d4f;color:white}
.pd-opt-val{font-size:15px;flex:1}.pd-opt-icon{color:#52c41a;font-size:18px}.pd-opt-icon.err{color:#ff4d4f}
.pd-result{padding:16px 20px;border-radius:10px;margin-bottom:20px}
.pd-result.ok{background:#f6ffed;border:1px solid #b7eb8f}.pd-result.err{background:#fff2f0;border:1px solid #ffccc7}
.pd-result-header{font-size:16px;font-weight:600;margin-bottom:6px}.pd-result-analysis{font-size:14px;line-height:1.7;color:#374151}
.pd-actions{display:flex;justify-content:space-between;align-items:center;margin-top:12px}
.pd-nav-btns{display:flex;align-items:center;gap:12px}.pd-nav-info{font-size:14px;color:#6b7280;font-weight:500}
.pd-summary{width:180px;background:white;border-left:1px solid #e5e7eb;padding:16px;overflow-y:auto;flex-shrink:0}
.pd-summary h4{font-size:13px;font-weight:600;color:#6b7280;margin-bottom:12px}
.pd-summary-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:5px}
.pd-s-cell{width:28px;height:28px;display:flex;align-items:center;justify-content:center;border-radius:4px;font-size:11px;font-weight:600;background:#f3f4f6;color:#9ca3af}
.pd-s-cell.done{background:#dbeafe;color:#4f7cff}.pd-s-cell.correct{background:#c8e6c9;color:#2e7d32}.pd-s-cell.wrong{background:#ffd6d6;color:#c62828}
.pd-s-cell.m-mastered{background:#c8e6c9;color:#2e7d32}.pd-s-cell.m-unfamiliar{background:#fff3e0;color:#e65100}.pd-s-cell.m-dontknow{background:#fce4ec;color:#c62828}.pd-s-cell.m-careless{background:#ede9fe;color:#6a1b9a}
.pd-legend{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px;font-size:11px;color:#9ca3af}
.pd-ld{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:3px;vertical-align:middle}
.pd-ld.active{background:#4f7cff}.pd-ld.done{background:#dbeafe}.pd-ld.correct{background:#c8e6c9}.pd-ld.wrong{background:#ffd6d6}
.pd-loading,.pd-empty-state{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:120px 0}
.pd-empty{text-align:center;padding:80px 0;color:#9ca3af}
.ph-settings-wrap{position:relative}.ph-settings-btn{background:none;border:none;cursor:pointer;padding:6px 8px;border-radius:6px;color:#9ca3af;display:flex;align-items:center}.ph-settings-btn:hover{background:#f0f4ff;color:#4f7cff}
.ph-settings-drop{position:absolute;top:40px;right:0;background:white;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.12);padding:14px 16px;z-index:200;width:180px}
.psd-item{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:#374151;margin-bottom:10px;gap:12px;white-space:nowrap}
.mastery-btns{display:flex;gap:4px}
</style>

<!-- unscoped for feedback animations -->
<style>
.feedback-float{position:fixed;z-index:9999;top:35%;font-size:32px;font-weight:900;pointer-events:none;animation:fb-slide 5s linear forwards;text-shadow:0 2px 12px rgba(0,0,0,.12);white-space:nowrap}
.fb-correct{color:#10b981;left:-200px}.fb-wrong{color:#ef4444;left:-200px}
@keyframes fb-slide{0%{transform:translateX(0);opacity:0}5%{opacity:1}80%{opacity:1}100%{opacity:0;transform:translateX(calc(100vw + 300px))}}
.pp-combo-badge{position:fixed;top:76px;left:50%;transform:translateX(-50%);z-index:80;padding:3px 10px;border-radius:10px;background:rgba(79,124,255,.08);font-size:12px;color:#4f7cff;font-weight:600}
.pp-float-combo{position:fixed;top:45%;left:50%;transform:translate(-50%,-50%);z-index:200;font-size:28px;font-weight:700;color:#4f7cff;text-shadow:0 2px 16px rgba(79,124,255,.25);pointer-events:none;animation:combo-pop .6s ease-out;white-space:nowrap;font-family:KaiTi,STKaiti,楷体,serif}
@keyframes combo-pop{0%{transform:translate(-50%,-50%) scale(.3);opacity:0}50%{transform:translate(-50%,-50%) scale(1.15);opacity:1}100%{transform:translate(-50%,-50%) scale(1);opacity:1}}
.pp-kb-hint{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:80;display:flex;gap:10px;padding:4px 14px;border-radius:20px;background:rgba(255,255,255,.5);backdrop-filter:blur(4px);font-size:10px;color:#c4c4c4;white-space:nowrap}
.pp-kb-hint span{opacity:.6}
</style>
