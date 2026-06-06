import pymysql, json

conn = pymysql.connect(host="localhost", user="root", password="123456", database="exam_platform", charset="utf8mb4", autocommit=True)
c = conn.cursor()

c.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ["question_knowledge","paper_question","exam_question","user_answer","wrong_question","favorite","note","exam_record","question"]:
    c.execute(f"DELETE FROM {t}")
c.execute("SET FOREIGN_KEY_CHECKS=1")
print("Cleared")

with open(r"D:\桌面\毕设\exam-platform\data\answers.json", "r", encoding="utf-8-sig") as f:
    answers = json.load(f)
with open(r"D:\桌面\毕设\exam-platform\data\all_comp_q.json", "r", encoding="utf-8") as f:
    comp_qs = json.load(f)
with open(r"D:\桌面\毕设\exam-platform\data\questions_raw.json", "r", encoding="utf-8") as f:
    raw_qs = json.load(f)

def get_chapter(text):
    kw = {
        5:["顺序表","链表","线性表","单链表","双链表","循环链表","头结点","头指针"],
        6:["栈","队列","出栈","入栈","出队","入队","循环队列","表达式"],
        7:["二叉树","二叉排序树","平衡二叉树","哈夫曼","遍历","前序","中序","后序","森林","叶结点","B树","完全"],
        8:["有向图","无向图","邻接","拓扑","最短路径","最小生成树","关键路径","Dijkstra","Floyd","Prim","Kruskal"],
        9:["散列","哈希","二分查找","折半","B+树","Hash","冲突","探测"],
        10:["排序","冒泡","快排","堆排序","归并","希尔","插入排序","选择排序","基数","小根堆","大根堆"],
        11:["补码","浮点","定点","IEEE","原码","反码","移码","阶码","规格化","溢出"],
        12:["Cache","主存","虚拟存储","DRAM","SRAM","编址","组相联","直接映射","全相联","命中"],
        13:["寻址","RISC","CISC","指令格式","指令字长"],
        14:["流水线","微程序","微指令","微操作","CPI","主频","冒险","数据通路"],
        15:["DMA","总线","程序中断","程序查询","通道","中断向量"],
        16:["进程","线程","死锁","银行家","PV操作","临界","时间片","抢占","优先级"],
        17:["分页","分段","页表","页面","缺页","FIFO","LRU","OPT","CLOCK","Belady"],
        18:["文件系统","目录","FCB","inode","索引文件","位示图"],
        19:["磁盘","SPOOLing","SSTF","SCAN","RAID"],
        20:["OSI","TCP/IP"],
        21:["曼彻斯特","奈奎斯特","香农"],
        22:["数据链路","CSMA","以太网","MAC","CRC","退避","碰撞","交换机"],
        23:["IP地址","路由","子网","CIDR","NAT","OSPF","RIP","IPv4","IPv6","ICMP","ARP"],
        24:["TCP","UDP","拥塞","滑动窗口","三次握手","四次挥手"],
        25:["HTTP","DNS","FTP","SMTP","应用层","Cookie","域名"],
    }
    best, bs = 5, 0
    for ch, kws in kw.items():
        s = sum(1 for k in kws if k in text)
        if s > bs: bs, best = s, ch
    return best

comp_ch_map = {101:5,102:6,103:7,104:8,105:9,106:10,203:12,204:13,205:14,301:16,302:16,303:17,304:18,305:19,403:22,404:23,405:24}

nid = 1
total = 0

# SINGLE 2009-2021 from questions_raw.json (array format)
for year_str in sorted(raw_qs.keys(), key=int):
    year = int(year_str)
    if year > 2021: continue
    qs = raw_qs[year_str]  # direct array
    for i, q in enumerate(qs[:40]):
        content = q.get("content", "")
        opts = q.get("options", {})
        raw_ans = q.get("answer", "")
        
        opt_list = [{"key":k,"value":opts[k]} for k in sorted(opts.keys())]
        opt_json = json.dumps(opt_list, ensure_ascii=False)
        
        ch = get_chapter(content)
        
        ans = raw_ans
        ka = answers.get(str(year),{}).get("answers",{}).get(str(i+1))
        if ka and ka in "ABCD": ans = ka
        if ans not in "ABCD": ans = "A"
        
        page = min((i // 5) + 1, 10)
        img = f'<img src=/images/questions/{year}_p{page:02d}.png style=max-width:100%;margin:8px 0;border-radius:6px loading=lazy />'
        
        c.execute(
            "INSERT INTO question (id,chapter_id,subject_id,type,difficulty,content,options,answer,analysis,year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (nid,ch,1,"SINGLE","MEDIUM",img,opt_json,ans,f"{year}年第{i+1}题",year))
        nid += 1; total += 1

print(f"SINGLE 2009-2021: {total}")

# SINGLE 2022-2025: screenshot only, correct answers
for year in range(2022, 2026):
    for i in range(40):
        page = min((i // 5) + 1, 8)
        img = f'<img src=/images/questions/{year}_p{page:02d}.png style=max-width:100%;margin:8px 0;border-radius:6px loading=lazy />'
        ans = "A"
        ka = answers.get(str(year),{}).get("answers",{}).get(str(i+1))
        if ka and ka in "ABCD": ans = ka
        c.execute(
            "INSERT INTO question (id,chapter_id,subject_id,type,difficulty,content,options,answer,analysis,year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (nid,5,1,"SINGLE","MEDIUM",img,"[]",ans,f"{year}年第{i+1}题",year))
        nid += 1; total += 1

print(f"+ SINGLE 2022-2025: {total}")

# COMPREHENSIVE 2009-2025
comp_n = 0
for year in range(2009, 2026):
    yqs = [q for q in comp_qs if q["y"]==year][:7]
    for i, q in enumerate(yqs):
        ch = comp_ch_map.get(q.get("ch",101), 5)
        page = 10 + i
        img = f'<img src=/images/questions/{year}_p{page:02d}.png style=max-width:100%;margin:8px 0;border-radius:6px loading=lazy /><br/>'
        content = img + q.get("c","")
        ans = q.get("a","")
        c.execute(
            "INSERT INTO question (id,chapter_id,subject_id,type,difficulty,content,options,answer,analysis,year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (nid,ch,1,"MULTI","HARD",content,"[]",ans,ans,year))
        nid += 1; total += 1; comp_n += 1

print(f"+ COMPREHENSIVE: {comp_n}")

# 2026 placeholder
for year in [2026]:
    for i in range(40):
        c.execute("INSERT INTO question (id,chapter_id,subject_id,type,difficulty,content,options,answer,analysis,year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (nid,5,1,"SINGLE","MEDIUM",f"2026年408真题 第{i+1}题（待更新）","[]","A","",year))
        nid += 1; total += 1
    for i in range(7):
        c.execute("INSERT INTO question (id,chapter_id,subject_id,type,difficulty,content,options,answer,analysis,year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (nid,5,1,"MULTI","HARD",f"2026年408真题 综合题第{i+1}题（待更新）","[]","","",year))
        nid += 1; total += 1

c.execute("SELECT COUNT(*) FROM question")
db_total = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM question WHERE content LIKE '%<img%'")
db_img = c.fetchone()[0]
print(f"\nDB: {db_total} questions, {db_img} with screenshots")
conn.close()
print("DONE!")
