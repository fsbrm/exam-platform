import pymysql, json

conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4", autocommit=True)
c = conn.cursor()

# Clear
c.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ["question_knowledge","paper_question","exam_question","user_answer","wrong_question","favorite","note","exam_record","question"]:
    c.execute(f"DELETE FROM {t}")
c.execute("SET FOREIGN_KEY_CHECKS=1")
print("Cleared")

# Load answers
with open(r"D:\桌面\毕设\exam-platform\data\answers.json", "r", encoding="utf-8-sig") as f:
    answers = json.load(f)

# Load comprehensive questions
with open(r"D:\桌面\毕设\exam-platform\data\all_comp_q.json", "r", encoding="utf-8") as f:
    comp_qs = json.load(f)

# Chapter keyword mapper
def get_chapter(text):
    kw = {
        5: ["顺序表","链表","线性表","单链表","双链表","循环链表","头结点","头指针","倒数第k"],
        6: ["栈","队列","出栈","入栈","出队","入队","循环队列","表达式求值"],
        7: ["二叉树","二叉排序树","平衡二叉树","哈夫曼","遍历","前序","中序","后序","层次","森林","叶结点","B树","完全"],
        8: ["有向图","无向图","邻接","拓扑排序","最短路径","最小生成树","关键路径","Dijkstra","Floyd","Prim","Kruskal"],
        9: ["散列","哈希","二分查找","折半","B+树","查找成功","查找失败","Hash","冲突","探测"],
        10: ["排序","冒泡","快排","堆排序","归并","希尔","插入排序","选择排序","基数","小根堆","大根堆"],
        11: ["补码","浮点","定点","IEEE","原码","反码","移码","阶码","尾数","规格化","溢出","海明码"],
        12: ["Cache","主存","虚拟存储","DRAM","SRAM","编址","地址映射","组相联","直接映射","全相联","命中"],
        13: ["寻址","操作码","RISC","CISC","指令格式","指令字长"],
        14: ["流水线","微程序","微指令","微操作","CPI","主频","MIPS","冒险","数据通路"],
        15: ["DMA","总线","程序中断","程序查询","通道","中断向量","中断屏蔽"],
        16: ["进程","线程","死锁","银行家","PV操作","临界","时间片","抢占","优先级","周转时间"],
        17: ["分页","分段","页表","页面","缺页","FIFO","LRU","OPT","CLOCK","Belady","段页式"],
        18: ["文件系统","目录","FCB","inode","索引文件","位示图"],
        19: ["磁盘调度","SPOOLing","SSTF","SCAN","RAID"],
        20: ["OSI","TCP/IP模型"],
        21: ["曼彻斯特","奈奎斯特","香农"],
        22: ["数据链路","CSMA","以太网","MAC地址","CRC","退避","碰撞","交换机","网桥"],
        23: ["IP地址","路由","子网掩码","CIDR","NAT","OSPF","RIP","BGP","IPv4","IPv6","ICMP","ARP"],
        24: ["TCP","UDP","拥塞","滑动窗口","三次握手","四次挥手","传输层"],
        25: ["HTTP","DNS","FTP","SMTP","应用层","万维网","Cookie","域名"],
    }
    best, best_s = 5, 0
    for ch, kws in kw.items():
        s = sum(1 for k in kws if k in text)
        if s > best_s:
            best_s, best = s, ch
    return best

# Chapter mapping for comprehensive questions
comp_ch_map = {101:5,102:6,103:7,104:8,105:9,106:10,203:12,204:13,205:14,301:16,302:16,303:17,304:18,305:19,403:22,404:23,405:24}

# Generate question IDs
next_id = 1

# SINGLE choice questions 2009-2021 from questions_raw.json
with open(r"D:\桌面\毕设\exam-platform\data\questions_raw.json", "r", encoding="utf-8") as f:
    raw_qs = json.load(f)

single_count = 0
for year_str, year_data in raw_qs.items():
    year = int(year_str)
    if year > 2021:
        continue
    
    qs = year_data.get("questions", year_data if isinstance(year_data, list) else [])
    if not qs:
        continue
    
    for i, q in enumerate(qs[:40]):
        content = q.get("content", "")
        options_obj = q.get("options", {})
        raw_answer = q.get("answer", "")
        
        # Build options JSON array
        opts = []
        for k in sorted(options_obj.keys()):
            opts.append({"key": k, "value": options_obj[k]})
        options_json = json.dumps(opts, ensure_ascii=False)
        
        # Get chapter
        ch = get_chapter(content)
        
        # Get correct answer
        ans = raw_answer
        if str(year) in answers:
            known = answers[str(year)].get("answers", {})
            ka = known.get(str(i+1))
            if ka and ka in "ABCD":
                ans = ka
        if ans not in "ABCD":
            ans = "A"
        
        # Page image
        page = min((i // 5) + 1, 10)
        img_tag = f'<img src=/images/questions/{year}_p{page:02d}.png style=max-width:100%;margin:8px 0;border-radius:6px loading=lazy />'
        
        full_content = img_tag
        analysis = f"{year}年408真题第{i+1}题"
        
        c.execute(
            "INSERT INTO question (id, chapter_id, subject_id, type, difficulty, content, options, answer, analysis, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (next_id, ch, 1, "SINGLE", "MEDIUM", full_content, options_json, ans, analysis, year)
        )
        next_id += 1
        single_count += 1

print(f"SINGLE 2009-2021: {single_count}")

# SINGLE for 2022-2025 (use screenshots only, no text content)
for year in range(2022, 2026):
    for i in range(40):
        page = min((i // 5) + 1, 8)
        img_tag = f'<img src=/images/questions/{year}_p{page:02d}.png style=max-width:100%;margin:8px 0;border-radius:6px loading=lazy />'
        
        ans = "A"
        if str(year) in answers:
            known = answers[str(year)].get("answers", {})
            ka = known.get(str(i+1))
            if ka and ka in "ABCD":
                ans = ka
        
        c.execute(
            "INSERT INTO question (id, chapter_id, subject_id, type, difficulty, content, options, answer, analysis, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (next_id, 5, 1, "SINGLE", "MEDIUM", img_tag, "[]", ans, f"{year}年408真题第{i+1}题", year)
        )
        next_id += 1
        single_count += 1

print(f"SINGLE total: {single_count}")

# COMPREHENSIVE questions 2009-2025
comp_count = 0
for year in range(2009, 2026):
    year_comps = [q for q in comp_qs if q["y"] == year]
    for i, q in enumerate(year_comps[:7]):
        ch = comp_ch_map.get(q["ch"], 5)
        page = 10 + i
        img_tag = f'<img src=/images/questions/{year}_p{page:02d}.png style=max-width:100%;margin:8px 0;border-radius:6px loading=lazy /><br/>'
        
        content = img_tag + q["c"]
        ans = q["a"]
        
        c.execute(
            "INSERT INTO question (id, chapter_id, subject_id, type, difficulty, content, options, answer, analysis, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (next_id, ch, 1, "MULTI", "HARD", content, "[]", ans, ans, year)
        )
        next_id += 1
        comp_count += 1

print(f"COMPREHENSIVE: {comp_count}")

# 2026 SINGLE + MULTI (AI-generated, keep minimal)
for year in [2026]:
    for i in range(40):
        c.execute(
            "INSERT INTO question (id, chapter_id, subject_id, type, difficulty, content, options, answer, analysis, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (next_id, 5, 1, "SINGLE", "MEDIUM", f"{year}年408真题 第{i+1}题（待更新）", "[]", "A", "", year)
        )
        next_id += 1
    for i in range(7):
        c.execute(
            "INSERT INTO question (id, chapter_id, subject_id, type, difficulty, content, options, answer, analysis, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (next_id, 5, 1, "MULTI", "HARD", f"{year}年408真题 综合题第{i+1}题（待更新）", "[]", "", "", year)
        )
        next_id += 1

c.execute("SELECT COUNT(*) FROM question")
total = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM question WHERE content LIKE '%<img%'")
img = c.fetchone()[0]
print(f"\nTotal: {total}, With screenshots: {img}")
conn.close()
print("Done!")
