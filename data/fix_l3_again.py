import os, re

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the entire L3 block using regex
old = r'''                  <div v-for="kp in ch\.knowledgePoints" :key="'k'\+kp\.id" class="kp-l3"
                    :class="\{ active: activeKP === kp\.id \}"
                    @click="selectKP\(kp\.id\)">
                    <span class="kp-l3-radio" :class="\{ checked: activeKP === kp\.id \}"></span>
                    <span class="kp-l3-name">\{\{ kp\.name \}\}</span>
                    <span v-if="activeKP === kp\.id" class="kp-l3-btn" @click\.stop="goPracticeByKP\(kp\.id\)">去刷题 &#8594;</span>
                    \s*</div>'''

# Actually let me just do a simpler string find on key parts
# Find the L3 section start
l3_start = content.find('<!-- Level 3: Knowledge Points -->')
l3_end = content.find('</div>\n                </div>\n              </div>\n            </div>\n          </div>\n        </div>', l3_start)

if l3_start < 0:
    print("L3 marker not found!")
else:
    print(f"L3 at position {l3_start}")

# Actually let me just do straight string replacement on the exact pattern
old_l3_block = '''<div v-for="kp in ch.knowledgePoints" :key="'k'+kp.id" class="kp-l3"
                    :class="{ active: activeKP === kp.id }"
                    @click="selectKP(kp.id)">
                    <span class="kp-l3-radio" :class="{ checked: activeKP === kp.id }"></span>
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span v-if="activeKP === kp.id" class="kp-l3-btn" @click.stop="goPracticeByKP(kp.id)">去刷题 &#8594;</span>
                    '''

new_l3_block = '''<div v-for="kp in ch.knowledgePoints" :key="'k'+kp.id" class="kp-l3"
                    :class="{ active: activeNode?.type==='kp' && activeNode?.id===kp.id }"
                    @click="selectNode('kp', kp.id)">
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span v-if="activeNode?.type==='kp' && activeNode?.id===kp.id" class="kp-btn" @click.stop="goPractice()">去刷题 &#8594;</span>
                    '''

if old_l3_block in content:
    content = content.replace(old_l3_block, new_l3_block)
    print("L3 block replaced successfully")
else:
    print("L3 block NOT FOUND - trying alternate")
    # Find and print what's actually there
    idx = content.find('kp-l3-radio')
    if idx >= 0:
        print("Found kp-l3-radio at", idx)
        print(repr(content[idx:idx+300]))
    # Try just replacing the class bindings
    content = content.replace(':class="{ active: activeKP === kp.id }"', ':class="{ active: activeNode?.type===\'kp\' && activeNode?.id===kp.id }"')
    content = content.replace('@click="selectKP(kp.id)"', '@click="selectNode(\'kp\', kp.id)"')
    content = content.replace('kp-l3-radio', 'kp-l3-radio-hidden')
    content = content.replace('kp-l3-btn', 'kp-btn')
    content = content.replace('goPracticeByKP(kp.id)', 'goPractice()')
    print("Fallback replacements done")

# Also remove radio dot CSS
content = content.replace('''.kp-l3-radio-hidden {
  width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0;
  border: 2px solid #d1d5db; transition: all 0.15s;
}
.kp-l3-radio-hidden.checked { border-color: #4f7cff; background: #4f7cff; box-shadow: inset 0 0 0 2px white; }
''', '/* radio removed */')

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")