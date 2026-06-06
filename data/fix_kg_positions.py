path = r'D:\桌面\毕设\exam-platform\frontend\src\views\knowledge\KnowledgeGraph.vue'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the echartsNodes mapping section and add x,y initial positions
# We need to find the pattern where nodes are constructed and add x/y coordinates

old_node_end = """      data: n
    }
  })"""

new_node_end = """      data: n
    }
  })

  // Assign initial positions based on category centers
  const catNodeCount: Record<string, number> = {}
  for (const n of echartsNodes) {
    const cat = n.data?.category || ''
    if (!catNodeCount[cat]) catNodeCount[cat] = 0
    catNodeCount[cat]++
  }
  let dsIdx = 0, coIdx = 0, osIdx = 0, cnIdx = 0
  for (const n of echartsNodes) {
    const cat = n.data?.category || ''
    if (cat === '数据结构') {
      n.x = catCenters['数据结构'][0] * 1000 + dsIdx * 20
      n.y = catCenters['数据结构'][1] * 1000 + (dsIdx % 5) * 30
      dsIdx++
    } else if (cat === '计算机组成原理') {
      n.x = catCenters['计算机组成原理'][0] * 1000 + coIdx * 20
      n.y = catCenters['计算机组成原理'][1] * 1000 + (coIdx % 5) * 30
      coIdx++
    } else if (cat === '操作系统') {
      n.x = catCenters['操作系统'][0] * 1000 + osIdx * 20
      n.y = catCenters['操作系统'][1] * 1000 + (osIdx % 5) * 30
      osIdx++
    } else {
      n.x = catCenters['计算机网络'][0] * 1000 + cnIdx * 20
      n.y = catCenters['计算机网络'][1] * 1000 + (cnIdx % 5) * 30
      cnIdx++
    }
  }"""

if old_node_end in content:
    content = content.replace(old_node_end, new_node_end)
    # Also reduce repulsion for a more compact layout
    content = content.replace('repulsion: 800', 'repulsion: 300')
    content = content.replace('gravity: 0.08', 'gravity: 0.04')
    content = content.replace('edgeLength: [80, 300]', 'edgeLength: [50, 160]')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added initial positions and reduced force distances')
else:
    print('Node pattern not found')