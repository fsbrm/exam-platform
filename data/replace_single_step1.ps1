# ============================================================
# Script: Replace 2009-2021 SINGLE questions with real scraped data
# ============================================================

$ErrorActionPreference = "Stop"

# === 1. Load real scraped questions ===
$r2 = Get-Content "D:\桌面\毕设\exam-platform\data\real_questions_v2.sql" -Encoding UTF8 -Raw

# Extract each question: (id, ch, subj, 'SINGLE', diff, 'content', 'options', 'answer', 'analysis', year)
$pattern = "\((\d+),\d+,\d+,'SINGLE','([^']*)','([^']*)','(\[[^\]]*\])','([A-D])','([^']*)',(\d{4})\)"
$realMatches = [regex]::Matches($r2, $pattern)

Write-Output "Found $($realMatches.Count) real scraped questions"

# === 2. Chapter keyword mapping ===
$chapterKeywords = @{
    5  = @('顺序表','链表','线性表','单链表','双链表','循环链表','头结点','头指针','顺序存储.*插入','顺序存储.*删除','倒数第k')
    6  = @('栈','队列','出栈','入栈','出队','入队','循环队列','表达式求值','运算符栈','操作数栈','后缀表达式','前缀表达式')
    7  = @('二叉树','二叉排序树','平衡二叉树','哈夫曼','遍历','前序','中序','后序','层次遍历','森林','叶结点','B树[^+]','B-树','完全二叉树','树.*结点','二叉查找树','AVL')
    8  = @('图','邻接','拓扑排序','最短路径','最小生成树','关键路径','Dijkstra','Floyd','Prim','Kruskal','深度优先搜索','广度优先搜索','连通分量','强连通')
    9  = @('散列','哈希','二分查找','折半查找','顺序查找','B\+树','查找成功','查找失败','Hash','冲突','开放定址','链地址')
    10 = @('排序','冒泡','快排','堆排序','归并','希尔','插入排序','选择排序','基数排序','交换排序','初始堆','小根堆','大根堆','一趟排序')
    11 = @('补码','浮点','定点','IEEE 754','进制','ALU','原码','反码','移码','规格化','溢出','算术移位')
    12 = @('Cache','主存','虚拟存储','DRAM','SRAM','存储.*编址','地址.*映射','组相联','直接映射','全相联','TLB','快表','页表','存储器','命中率')
    13 = @('指令系统','寻址方式','操作码','地址码','RISC','CISC','指令格式','立即寻址','直接寻址','间接寻址','变址寻址','相对寻址','基址寻址','指令字')
    14 = @('CPU','流水线','微程序','控制器','数据通路','微指令','微操作','指令周期','机器周期','时钟周期','冒险','结构冒险','数据冒险','控制冒险','转发')
    15 = @('总线','DMA','中断','I/O','输入输出','程序查询','程序中断','通道','接口','外部设备')
    16 = @('进程','线程','死锁','调度','同步','互斥','信号量','银行家','PV操作','临界区','并发','管程','时间片','优先级','抢占')
    17 = @('分页','分段','页表','页面','缺页','虚拟.*地址','地址转换','页框','页内偏移','FIFO','LRU','OPT','CLOCK','Belady','内存.*管理','请求分页','段页式')
    18 = @('文件.*系统','目录','FCB','inode','索引.*文件','文件.*分配','文件.*保护','文件.*共享','磁盘块','混合索引')
    19 = @('磁盘.*调度','SPOOLing','设备.*管理','I/O.*控制','电梯算法','SSTF','SCAN','C-SCAN','磁盘臂','RAID')
    20 = @('OSI','TCP/IP模型','网络体系')
    21 = @('物理层','编码.*传输','曼彻斯特','差分曼彻斯特','奈奎斯特','香农','信噪比')
    22 = @('数据链路','帧','CSMA','以太网','交换机','MAC','CRC','差错控制','流量控制','停等','GBN','选择重传','HDLC','PPP','退避','碰撞','冲突检测')
    23 = @('IP地址','路由','子网','CIDR','NAT','OSPF','RIP','BGP','IPv4','IPv6','网络层','路由器','子网掩码','ICMP','ARP','DHCP')
    24 = @('TCP','UDP','传输层','拥塞控制','滑动窗口','序号.*确认','三次握手','四次挥手','慢开始','拥塞避免','快重传','快恢复')
    25 = @('HTTP','DNS','FTP','SMTP','应用层','电子邮件','万维网','URL','Cookie','Web','域名')
}

function Map-Chapter($content) {
    $scores = @{}
    foreach ($ch in $chapterKeywords.Keys) {
        $score = 0
        foreach ($kw in $chapterKeywords[$ch]) {
            if ($content -match $kw) { $score++ }
        }
        if ($score -gt 0) { $scores[$ch] = $score }
    }
    if ($scores.Count -eq 0) { return 5 }  # default to 线性表
    # Return chapter with highest score
    return ($scores.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 1).Key
}

# === 3. Load known answers ===
$answersJson = Get-Content "D:\桌面\毕设\exam-platform\data\answers.json" -Encoding UTF8 -Raw | ConvertFrom-Json

# === 4. Process each real question ===
$realQuestions = @()
$errors = @()
$chapterCounts = @{}

foreach ($m in $realMatches) {
    $id = [int]$m.Groups[1].Value
    $diff = $m.Groups[2].Value
    $content = $m.Groups[3].Value -replace "'", "''"
    $options = $m.Groups[4].Value
    $answer = $m.Groups[5].Value
    $analysis = $m.Groups[6].Value -replace "'", "''"
    $year = [int]$m.Groups[7].Value
    
    # Map chapter
    $chapter = Map-Chapter $content
    if (-not $chapterCounts[$chapter]) { $chapterCounts[$chapter] = 0 }
    $chapterCounts[$chapter]++
    
    # Correct answer if known
    $correctAnswer = $answer
    $ansSource = "scraped"
    if ($answersJson."$year" -and $answersJson."$year".answers) {
        # We don't know the question number, use content matching instead
        $correctAnswer = $answer  # Keep scraped answer for now
    }
    
    $realQuestions += @{
        year = $year
        chapter = $chapter
        diff = $diff
        content = $content
        options = $options
        answer = $correctAnswer
        analysis = $analysis
    }
}

Write-Output "`nChapter distribution:"
$chapterCounts.GetEnumerator() | Sort-Object Name | ForEach-Object { Write-Output "  Ch $($_.Key): $($_.Value)" }

# Group by year
$byYear = $realQuestions | Group-Object { $_.year } | Sort-Object Name
Write-Output "`nReal questions by year:"
foreach ($g in $byYear) { Write-Output "  $($g.Name): $($g.Count)" }

Write-Output "`nTotal: $($realQuestions.Count)"
