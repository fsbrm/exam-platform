# ============================================================
# Replace 2009-2021 SINGLE questions with real scraped content
# in seed-v4.sql -> seed-v5.sql
# ============================================================

$seed = Get-Content "D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v4.sql" -Encoding UTF8 -Raw
$r2 = Get-Content "D:\桌面\毕设\exam-platform\data\real_questions_v2.sql" -Encoding UTF8 -Raw
$ansJson = Get-Content "D:\桌面\毕设\exam-platform\data\answers.json" -Encoding UTF8 -Raw | ConvertFrom-Json

# Extract real SINGLE questions by year
$realByYear = @{}
$pattern = "\((\d+),\d+,\d+,'SINGLE'(.*?),(\d{4})\)"
$allM = [regex]::Matches($r2, $pattern)
foreach ($m in $allM) {
    $y = [int]$m.Groups[3].Value
    if (-not $realByYear[$y]) { $realByYear[$y] = @() }
    # Extract just the tail part: 'content','options','answer','analysis' 
    # The full match is: (id,1,1,'SINGLE','content','options','answer','analysis',year)
    $tail = $m.Groups[2].Value  # starts with ,'content'...
    $realByYear[$y] += $tail
}

Write-Output "Real questions loaded. Years: $($realByYear.Keys.Count)"
foreach ($y in ($realByYear.Keys | Sort-Object)) {
    Write-Output "  $y`: $($realByYear[$y].Count)"
}

# === Keyword chapter matcher ===
$kw = @{
    5  = @('顺序表','链表','线性表','单链表','双链表','循环链表','头结点','头指针','倒数第k')
    6  = @('栈','队列','出栈','入栈','出队','入队','循环队列','表达式求值')
    7  = @('二叉树','二叉排序树','平衡二叉树','哈夫曼','遍历','前序','中序','后序','层次','森林','叶结点','B树[^+*]','B-树','完全','二叉.*深度')
    8  = @('有向图','无向图','邻接','拓扑排序','最短路径','最小生成树','关键路径','Dijkstra','Floyd','Prim','Kruskal')
    9  = @('散列','哈希','二分查找','折半','顺序查找','B\+树','查找成功','查找失败','Hash','冲突','探测')
    10 = @('排序','冒泡','快排','堆排序','归并','希尔','插入排序','选择排序','基数','小根堆','大根堆','一趟排序')
    11 = @('补码','浮点','定点','IEEE','进制|原码','反码|移码|阶码|尾数','规格化')
    12 = @('Cache','主存','虚拟存储','DRAM','SRAM','编址','地址.*映射','组相联','直接映射','全相联','命中','主存块','Cache行')
    13 = @('寻址','RISC|CISC','指令格式','指令字长','扩展操作码')
    14 = @('流水线','微程序','微指令','微操作','CPI|主频|MIPS','冒险')
    15 = @('DMA','总线','程序中断','程序查询','通道|中断向量','中断屏蔽|中断响应')
    16 = @('进程|线程','死锁|银行家','PV操作|临界','时间片|抢占|优先级','周转时间|调度算法')
    17 = @('分页|分段|页表|页面|缺页','FIFO|LRU|OPT|CLOCK|Belady','段页式|交换|覆盖')
    18 = @('文件.*系统|目录|FCB|inode','索引.*文件|文件.*分配|位示图')
    19 = @('磁盘.*调度|SPOOLing|SSTF|SCAN|RAID')
    20 = @('OSI|TCP/IP.*模型')
    21 = @('物理层|曼彻斯特|奈奎斯特|香农')
    22 = @('数据链路|CSMA|以太网.*MAC|CRC|退避|碰撞|交换机|网桥|GBN')
    23 = @('IP地址|路由|子网.*掩码|CIDR|NAT|OSPF|RIP|BGP|IPv4|IPv6|ICMP|ARP|DHCP')
    24 = @('TCP|UDP|拥塞|滑动窗口|三次握手|四次挥手|传输层')
    25 = @('HTTP|DNS|FTP|SMTP|应用层|万维网|Cookie|域名')
}

function Get-BestChapter($text) {
    $best = 5; $bestScore = 0
    foreach ($ch in $kw.Keys) {
        $score = 0
        foreach ($k in $kw[$ch]) { 
            # Support pipe-separated keywords
            $parts = $k -split '\|'
            foreach ($part in $parts) {
                if ($text -match $part) { $score++ }
            }
        }
        if ($score -gt $bestScore) { $bestScore = $score; $best = $ch }
    }
    return $best
}

# === Build replacement map ===
# For each year, map SINGLE question ID -> new content
$replacements = @{}  # id -> new SQL line suffix

# Get existing SINGLE IDs per year from seed-v4
$seedSingles = @{}
$sp = "\((\d+),(\d+),(\d+),'SINGLE','([^']*)','([^']*)','(\[[^\]]*\])','([^']*)','([^']*)',(\d{4})\)"
$sm = [regex]::Matches($seed, $sp)
foreach ($m in $sm) {
    $id = [int]$m.Groups[1].Value
    $ch = [int]$m.Groups[2].Value
    $y = [int]$m.Groups[9].Value
    if (-not $seedSingles[$y]) { $seedSingles[$y] = @() }
    $seedSingles[$y] += @{id=$id; ch=$ch; full=$m.Value}
}

# Now for each year with real data, replace content
$replaced = 0
$skipped = 0

for ($year = 2009; $year -le 2021; $year++) {
    $realQs = $realByYear[$year]
    $seedQs = $seedSingles[$year]
    if (-not $realQs -or -not $seedQs) { continue }
    
    $n = [Math]::Min($realQs.Count, $seedQs.Count)
    Write-Output "`nProcessing $year: real=$($realQs.Count), seed=$($seedQs.Count), replacing first $n"
    
    for ($i = 0; $i -lt $n; $i++) {
        $sid = $seedQs[$i].id
        $sch = $seedQs[$i].ch
        $realTail = $realQs[$i]
        $full = $seedQs[$i].full
        
        # Parse real tail to get content, options, answer, analysis
        # Format: ,'DIFF','CONTENT','OPTIONS','ANSWER','ANALYSIS'
        if ($realTail -match ",'([^']*)','([^']*)','(\[[^\]]*\])','([^']*)','([^']*)'") {
            $diff = $Matches[1]
            $content = $Matches[2] -replace "'", "''"
            $options = $Matches[3]
            $rAnswer = $Matches[4]
            $analysis = $Matches[5] -replace "'", "''"
            
            # Map chapter
            $bestCh = Get-BestChapter $content
            
            # Fix answer: prefer answers.json
            $finalAnswer = $rAnswer
            $qNum = $i + 1
            $knownYear = $ansJson."$year"
            if ($knownYear -and $knownYear.answers) {
                $knownAns = $knownYear.answers."$qNum"
                if ($knownAns -and $knownAns -match '^[A-D]$') {
                    $finalAnswer = $knownAns
                }
            }
            
            # If scraped answer is empty, use known
            if ($rAnswer -eq '' -and $knownAns -and $knownAns -match '^[A-D]$') {
                $finalAnswer = $knownAns
            }
            
            # Build replacement full tuple
            $newFull = "($sid,$bestCh,1,'SINGLE','$diff','$content','$options','$finalAnswer','$analysis',$year)"
            
            # Replace in seed
            $seed = $seed -replace [regex]::Escape($full), $newFull
            $replaced++
        } else {
            $skipped++
            Write-Output "  Skip Q$($i+1) - could not parse"
        }
    }
}

Write-Output "`n=== Results ==="
Write-Output "Replaced: $replaced, Skipped: $skipped"

# Save
$seed | Out-File -FilePath "D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v5.sql" -Encoding UTF8 -NoNewline

# Quick verify
$v5 = Get-Content "D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v5.sql" -Encoding UTF8 -Raw
$sCount = ([regex]::Matches($v5, "'SINGLE'")).Count
$mCount = ([regex]::Matches($v5, "'MULTI'")).Count
Write-Output "Seed-v5: SINGLE=$sCount, MULTI=$mCount, Total=$($sCount+$mCount)"
$size = (Get-Item "D:\桌面\毕设\exam-platform\backend\src\main\resources\db\migration\seed-v5.sql").Length
Write-Output "Size: $size bytes"

