import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: toggleKP -> selectKP
content = content.replace('@click="toggleKP(kp.id)"', '@click="selectKP(kp.id)"')

# Fix 2: Replace old L3 span with radio + floating button
old_l3_span = '''<span class="kp-l3-dot" :style="{background: activeKP === kp.id ? '#4f7cff' : '#d1d5db'}"></span>
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    '''

new_l3_span = '''<span class="kp-l3-radio" :class="{ checked: activeKP === kp.id }"></span>
                    <span class="kp-l3-name">{{ kp.name }}</span>
                    <span v-if="activeKP === kp.id" class="kp-l3-btn" @click.stop="goPracticeByKP(kp.id)">去刷题 &#8594;</span>
                    '''

content = content.replace(old_l3_span, new_l3_span)

# Fix 3: Make sure the goPracticeByKP function exists and works
# Check if it calls the right endpoint
if 'function goPracticeByKP' in content:
    print("goPracticeByKP exists")
else:
    print("WARNING: goPracticeByKP missing!")

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("L3 template fixed")