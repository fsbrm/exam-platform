import os

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "src", "views", "papers", "PapersPage.vue"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change selection style: blue border box instead of background
old = '.kp-l1-header.selected, .kp-l2-header.selected, .kp-l3.active { background: #eff6ff; border-radius: 6px; }'
new = '.kp-l1-header.selected, .kp-l2-header.selected { border: 2px solid #4f7cff; border-radius: 8px; padding: 6px; }'
content = content.replace(old, new)

# Add L3 selected style separately
old_l3_style = '.kp-l3 {'
new_l3_style = '.kp-l3.active { border: 2px solid #4f7cff; border-radius: 6px; }\n.kp-l3 {'
content = content.replace(old_l3_style, new_l3_style)

# 2. Add onActivated to reload data when coming back (refresh mastery)
old_onmounted_end = '''    }
  } catch {}
})'''

new_onmounted_end = '''    }
  } catch {}
})

// Reload matrix data when component is activated (e.g., returning from question page)
import { onActivated } from 'vue'
onActivated(async () => {
  try {
    const res: any = await api.get('/papers/matrix?subjectId=1')
    if (res.code === 200) {
      matrixData.value = res.data.years || []
    }
  } catch {}
})'''

content = content.replace(old_onmounted_end, new_onmounted_end)

# But wait, onActivated only works with <keep-alive>. Let me use a different approach.
# Instead, just remove the keep-alive approach and add a simple reload flag
# Actually, since Vue Router reuses components by default in SPA, the onMounted won't re-fire.
# Let me add a watch on the route instead.

# Remove the onActivated attempt (it won't work without keep-alive)
old_activated = '''// Reload matrix data when component is activated (e.g., returning from question page)
import { onActivated } from 'vue'
onActivated(async () => {
  try {
    const res: any = await api.get('/papers/matrix?subjectId=1')
    if (res.code === 200) {
      matrixData.value = res.data.years || []
    }
  } catch {}
})'''

content = content.replace(old_activated, '''// Data reloads on each navigation via router''')

# 3. Add router navigation guard to reload data
# Use beforeRouteEnter equivalent - simpler: just add a mounted watcher
# Actually the simplest fix: make the homepage or back-navigation always trigger a fresh load.
# Let me add a key to the router-view instead. Better yet, let me just make the component
# reload data whenever it becomes visible.

# Add a simple approach: watch the route and reload
old_import = "import { useRouter } from 'vue-router'"
new_import = "import { useRouter, useRoute } from 'vue-router'"
content = content.replace(old_import, new_import)

# Add watch for route changes
if 'const router = useRouter()' in content and 'const route = useRoute()' not in content:
    content = content.replace('const router = useRouter()', 'const router = useRouter()\nconst route = useRoute()')

# Add import for watch
if "import { ref, computed, reactive, onMounted } from 'vue'" in content:
    content = content.replace(
        "import { ref, computed, reactive, onMounted } from 'vue'",
        "import { ref, computed, reactive, onMounted, watch } from 'vue'"
    )

# Add watch to reload on route changes
old_final = '// Data reloads on each navigation via router'
new_final = '''// Reload data on navigation
watch(() => route.path, async (newPath) => {
  if (newPath === '/papers') {
    try {
      const res: any = await api.get('/papers/matrix?subjectId=1')
      if (res.code === 200) {
        matrixData.value = res.data.years || []
      }
    } catch {}
  }
})'''

# Actually let me just replace the old comment
content = content.replace(old_final, new_final)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Selection style: blue border + data reload on navigation")