filepath = r'D:\桌面\毕设\exam-platform\frontend\src\views\practice\PracticePage.vue'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the SINGLE MODE section and replace with 3-column layout
# The single mode starts with: <!-- SINGLE MODE -->
old_single_start = '      <!-- SINGLE MODE -->'
old_single_end = '    </div>\n  </div>\n</template>'

# Find the section
start_idx = content.find(old_single_start)
end_idx = content.find(old_single_end)

# Build the new 3-column single mode
new_single = '''      <!-- SINGLE MODE: 3-column layout -->
      <div v-if="viewMode === 'single' && currentQuestion" class="single-layout">
        <!-- Left: Question Navigator -->
        <nav class="sl-nav">
          <div class="sl-nav-title">题号导航</div>
          <div class="sl-nav-grid">
            <div v-for="(q, idx) in choiceQuestions" :key="q.id"
              class="sl-nav-num"
              :class="{
                active: currentIndex === questions.indexOf(q),
                correct: q._correct === true,
                wrong: q._correct === false,
                done: q._submitted
              }"
              @click="currentIndex = questions.indexOf(q); loadAnswer(questions.indexOf(q))">
              {{ idx + 1 }}
            </div>
          </div>
          <div class="sl-nav-legend">
            <span><i class="sln-dot done"></i>已答</span>
            <span><i class="sln-dot correct"></i>正确</span>
            <span><i class="sln-dot wrong"></i>错误</span>
          </div>
        </nav>

        <!-- Center: Question -->
        <main class="sl-main">
          <div class="sl-q-card">
            <div class="sl-q-header">
              <el-button text @click="goBack" class="back-btn"><el-icon><ArrowLeft /></el-icon>返回</el-button>
              <el-tag :type="typeTagType">{{ typeLabel }}</el-tag>
              <el-tag :type="diffTagType" effect="plain">{{ diffLabel }}</el-tag>
              <span class="sl-q-num">第{{ currentIndex + 1 }}/{{ questions.length }} 题</span>
              <div class="mastery-btns">
                <el-button :type="currentMastery === 'mastered' ? 'success' : ''" size="small" plain @click="markMastery('mastered')">掌握</el-button>
                <el-button :type="currentMastery === 'unfamiliar' ? 'warning' : ''" size="small" plain @click="markMastery('unfamiliar')">不熟</el-button>
                <el-button :type="currentMastery === 'dontknow' ? 'danger' : ''" size="small" plain @click="markMastery('dontknow')">不会</el-button>
              </div>
              <el-button text :icon="isFavorited ? 'StarFilled' : 'Star'" @click="toggleFavorite" class="fav-btn">
                {{ isFavorited ? '已收藏' : '收藏' }}
              </el-button>
            </div>

            <div class="sl-q-content" v-html="renderedContent"></div>

            <!-- Options -->
            <div class="sl-options" v-if="['SINGLE', 'MULTI'].includes(currentQuestion.type)">
              <div v-for="opt in parsedOptions" :key="opt.key"
                class="sl-opt"
                :class="{
                  selected: isSelected(opt.key),
                  correct: showResult && opt.key === correctAnswer,
                  wrong: showResult && isSelected(opt.key) && opt.key !== correctAnswer,
                  disabled: showResult
                }"
                @click="selectOption(opt.key)">
                <span class="sl-opt-key">{{ opt.key }}</span>
                <span class="sl-opt-val">{{ opt.value }}</span>
              </div>
            </div>

            <div class="sl-options" v-if="currentQuestion.type === 'JUDGE'">
              <div v-for="opt in [{key:'T',value:'正确'},{key:'F',value:'错误'}]" :key="opt.key"
                class="sl-opt"
                :class="{
                  selected: selectedAnswer === opt.key,
                  correct: showResult && opt.key === correctAnswer,
                  wrong: showResult && selectedAnswer === opt.key && opt.key !== correctAnswer,
                  disabled: showResult
                }"
                @click="selectOption(opt.key)">
                <span class="sl-opt-key">{{ opt.key === 'T' ? '✓' : '✗' }}</span>
                <span class="sl-opt-val">{{ opt.value }}</span>
              </div>
            </div>

            <div class="sl-fill" v-if="currentQuestion.type === 'FILL'">
              <el-input v-model="selectedAnswer" placeholder="请输入答案" :disabled="showResult" size="large" />
            </div>

            <!-- Comprehensive answer -->
            <div v-if="currentQuestion?.type === 'COMPREHENSIVE'" class="sl-result ok">
              <div class="sl-result-hd">📝 参考答案</div>
              <div class="sl-result-body" v-html="currentQuestion.answer"></div>
              <div class="sl-result-body" v-if="currentQuestion.analysis" v-html="currentQuestion.analysis" style="margin-top:8px"></div>
            </div>

            <!-- Result -->
            <div v-if="showResult" class="sl-result" :class="{ ok: lastCorrect, err: !lastCorrect }">
              <div class="sl-result-hd">
                <span>{{ lastCorrect ? '✅ 回答正确！' : '❌ 回答错误' }}</span>
                <span v-if="!lastCorrect" style="margin-left:8px">正确答案：<strong>{{ correctAnswer }}</strong></span>
              </div>
              <div class="sl-result-body" v-if="currentQuestion.analysis" v-html="renderText(currentQuestion.analysis)"></div>
            </div>

            <!-- Actions -->
            <div class="sl-actions">
              <el-button @click="prevQuestion" :disabled="currentIndex === 0" size="large"><el-icon><ArrowLeft /></el-icon>上一题</el-button>
              <el-button v-if="!showResult && canSubmit" type="primary" size="large" @click="submitAnswer">提交答案</el-button>
              <el-button v-if="showResult && currentIndex < questions.length - 1" type="primary" size="large" @click="nextQuestion">下一题<el-icon><ArrowRight /></el-icon></el-button>
              <el-button v-if="showResult && currentIndex === questions.length - 1" type="success" size="large" @click="finishPractice">完成练习</el-button>
              <el-button v-if="showResult" @click="openAiChat">🤖 AI帮我分析</el-button>
            </div>
          </div>
        </main>

        <!-- Right: Answer Sheet -->
        <aside class="sl-sheet">
          <div class="sl-sheet-title">答题卡</div>
          <div class="sl-sheet-grid">
            <div v-for="(q, idx) in choiceQuestions" :key="'s'+q.id"
              class="sl-sheet-cell"
              :class="{
                done: q._submitted,
                correct: q._correct === true,
                wrong: q._correct === false,
                active: currentIndex === questions.indexOf(q)
              }"
              @click="currentIndex = questions.indexOf(q); loadAnswer(questions.indexOf(q))">
              {{ idx + 1 }}
            </div>
          </div>
          <div class="sl-sheet-legend">
            <span><i class="ssl-dot active"></i>当前</span>
            <span><i class="ssl-dot done"></i>已答</span>
            <span><i class="ssl-dot correct"></i>正确</span>
            <span><i class="ssl-dot wrong"></i>错误</span>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>'''

content = content[:start_idx] + new_single

# Also update list mode to filter comprehensive questions
# In list mode: filter out COMPREHENSIVE, only show 选择题
content = content.replace(
    '<div v-for="(q, qi) in questions" :key="q.id" class="pl-card" :id="\'q-\'+q.id">',
    '<div v-for="(q, qi) in questions.filter(q => q.type !== \'COMPREHENSIVE\')" :key="q.id" class="pl-card" :id="\'q-\'+q.id">'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Template updated! Adding computed property for choiceQuestions...')
