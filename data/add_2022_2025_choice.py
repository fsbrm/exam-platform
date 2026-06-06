import pymysql, random

conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cursor = conn.cursor()

# Get existing knowledge points per chapter for linking
def get_kp(chapter_id):
    cursor.execute('SELECT id FROM knowledge_point WHERE chapter_id=%s LIMIT 1', (chapter_id,))
    r = cursor.fetchone()
    return r[0] if r else None

# Question templates for 2022-2025
# Each year gets ~15 choice questions spread across subjects
questions_extra = []

# Helper: year, content, options (JSON array), answer, chapter_id, subject_id, difficulty
def add_q(year, content, opts, ans, ch, subj, diff='MEDIUM'):
    import json
    questions_extra.append((year, content, json.dumps(opts, ensure_ascii=False), ans, ch, subj, diff))

# ===== 2022 Choice Questions =====
# 数据结构
add_q(2022, "下列排序算法中，在最好情况下时间复杂度为O(n)的是（ ）。",
      [{"key":"A","value":"快速排序"},{"key":"B","value":"归并排序"},{"key":"C","value":"冒泡排序"},{"key":"D","value":"堆排序"}], "C", 106, 10, 'EASY')
add_q(2022, "在一个具有n个结点的有序单链表中插入一个新结点并仍然保持有序的时间复杂度是（ ）。",
      [{"key":"A","value":"O(1)"},{"key":"B","value":"O(n)"},{"key":"C","value":"O(logn)"},{"key":"D","value":"O(nlogn)"}], "B", 101, 10, 'EASY')
add_q(2022, "设栈的输入序列为1,2,3,4，则不可能得到的输出序列是（ ）。",
      [{"key":"A","value":"1,2,3,4"},{"key":"B","value":"4,3,2,1"},{"key":"C","value":"1,4,3,2"},{"key":"D","value":"4,3,1,2"}], "D", 102, 10, 'EASY')
add_q(2022, "一棵完全二叉树有1000个结点，则其叶子结点数为（ ）。",
      [{"key":"A","value":"499"},{"key":"B","value":"500"},{"key":"C","value":"501"},{"key":"D","value":"502"}], "B", 103, 10, 'MEDIUM')
# 计算机组成原理
add_q(2022, "在Cache的地址映射中，组相联映射是（ ）的结合。",
      [{"key":"A","value":"直接映射与全相联映射"},{"key":"B","value":"直接映射与段式映射"},{"key":"C","value":"全相联映射与页式映射"},{"key":"D","value":"段式映射与页式映射"}], "A", 203, 20, 'EASY')
add_q(2022, "CPU响应中断时，保护现场的工作是（ ）。",
      [{"key":"A","value":"由硬件自动完成"},{"key":"B","value":"由中断服务程序完成"},{"key":"C","value":"由操作系统完成"},{"key":"D","value":"由编译程序完成"}], "B", 205, 20, 'MEDIUM')
add_q(2022, "微程序控制器中，机器指令与微指令的关系是（ ）。",
      [{"key":"A","value":"一条机器指令由一段微指令编的程序来解释执行"},{"key":"B","value":"一段机器指令组成的程序可由一条微指令来执行"},{"key":"C","value":"一条微指令由若干条机器指令组成"},{"key":"D","value":"每条机器指令由一条微指令来执行"}], "A", 205, 20, 'EASY')
add_q(2022, "补码表示的8位二进制整数中，-128的补码是（ ）。",
      [{"key":"A","value":"10000000"},{"key":"B","value":"11111111"},{"key":"C","value":"00000000"},{"key":"D","value":"01111111"}], "A", 202, 20, 'EASY')
# 操作系统
add_q(2022, "在操作系统中，产生死锁的四个必要条件不包括（ ）。",
      [{"key":"A","value":"互斥条件"},{"key":"B","value":"请求与保持条件"},{"key":"C","value":"不可剥夺条件"},{"key":"D","value":"同步条件"}], "D", 302, 30, 'EASY')
add_q(2022, "在请求分页系统中，页面置换算法中不会出现Belady异常的是（ ）。",
      [{"key":"A","value":"FIFO"},{"key":"B","value":"LRU"},{"key":"C","value":"CLOCK"},{"key":"D","value":"所有算法都会"}], "B", 303, 30, 'MEDIUM')
add_q(2022, "进程从运行态进入就绪态的原因是（ ）。",
      [{"key":"A","value":"等待某一事件"},{"key":"B","value":"时间片用完"},{"key":"C","value":"被选中占有CPU"},{"key":"D","value":"等待的事件已发生"}], "B", 301, 30, 'EASY')
# 计算机网络
add_q(2022, "TCP协议中，发送窗口的大小取决于（ ）。",
      [{"key":"A","value":"接收方窗口和拥塞窗口的较大值"},{"key":"B","value":"接收方窗口和拥塞窗口的较小值"},{"key":"C","value":"仅接收方窗口"},{"key":"D","value":"仅拥塞窗口"}], "B", 405, 40, 'MEDIUM')
add_q(2022, "OSPF协议使用的路由算法是（ ）。",
      [{"key":"A","value":"距离向量算法"},{"key":"B","value":"链路状态算法"},{"key":"C","value":"路径向量算法"},{"key":"D","value":"洪泛算法"}], "B", 404, 40, 'EASY')
add_q(2022, "IPv6地址的长度是（ ）位。",
      [{"key":"A","value":"32"},{"key":"B","value":"64"},{"key":"C","value":"128"},{"key":"D","value":"256"}], "C", 404, 40, 'EASY')
add_q(2022, "以太网交换机根据（ ）转发数据帧。",
      [{"key":"A","value":"IP地址"},{"key":"B","value":"MAC地址"},{"key":"C","value":"端口号"},{"key":"D","value":"域名"}], "B", 403, 40, 'EASY')

# ===== 2023 Choice Questions =====
add_q(2023, "一个有n个结点的无向图，其生成树有（ ）条边。",
      [{"key":"A","value":"n"},{"key":"B","value":"n-1"},{"key":"C","value":"n+1"},{"key":"D","value":"2n"}], "B", 104, 10, 'EASY')
add_q(2023, "二分查找（折半查找）要求查找表是（ ）。",
      [{"key":"A","value":"顺序存储且有序"},{"key":"B","value":"链式存储且有序"},{"key":"C","value":"顺序存储"},{"key":"D","value":"链式存储"}], "A", 105, 10, 'EASY')
add_q(2023, "下列哪种数据结构最适合实现递归调用？（ ）",
      [{"key":"A","value":"队列"},{"key":"B","value":"栈"},{"key":"C","value":"数组"},{"key":"D","value":"链表"}], "B", 102, 10, 'EASY')
add_q(2023, "哈希表中出现冲突时，线性探测法属于（ ）。",
      [{"key":"A","value":"开放定址法"},{"key":"B","value":"链地址法"},{"key":"C","value":"再哈希法"},{"key":"D","value":"公共溢出区法"}], "A", 105, 10, 'MEDIUM')
add_q(2023, "冯诺依曼计算机工作方式的基本特点是（ ）。",
      [{"key":"A","value":"多指令流单数据流"},{"key":"B","value":"按地址访问并顺序执行指令"},{"key":"C","value":"堆栈操作"},{"key":"D","value":"存储器按内容选择地址"}], "B", 201, 20, 'EASY')
add_q(2023, "流水线CPU中，下列哪种数据冒险可以通过转发技术解决？（ ）",
      [{"key":"A","value":"RAW（写后读）"},{"key":"B","value":"WAR（读后写）"},{"key":"C","value":"WAW（写后写）"},{"key":"D","value":"结构冒险"}], "A", 205, 20, 'MEDIUM')
add_q(2023, "DMA方式的数据传送是在（ ）之间进行的。",
      [{"key":"A","value":"CPU与主存"},{"key":"B","value":"外设与外设"},{"key":"C","value":"外设与主存"},{"key":"D","value":"CPU与外设"}], "C", 206, 20, 'EASY')
add_q(2023, "相对寻址方式中，操作数的有效地址是（ ）。",
      [{"key":"A","value":"基址寄存器内容加上位移量"},{"key":"B","value":"变址寄存器内容加上位移量"},{"key":"C","value":"程序计数器PC的内容加上位移量"},{"key":"D","value":"指令中直接给出的地址"}], "C", 204, 20, 'EASY')
add_q(2023, "在操作系统中，临界区是指（ ）。",
      [{"key":"A","value":"用于实现进程互斥的信号量"},{"key":"B","value":"进程中访问临界资源的那段代码"},{"key":"C","value":"一个缓冲区"},{"key":"D","value":"一段共享数据区"}], "B", 302, 30, 'EASY')
add_q(2023, "位示图可用于（ ）。",
      [{"key":"A","value":"文件目录的查找"},{"key":"B","value":"磁盘空间的管理"},{"key":"C","value":"主存空间的分配"},{"key":"D","value":"实现文件的保护和保密"}], "B", 304, 30, 'MEDIUM')
add_q(2023, "分页存储管理中，页面大小由（ ）决定。",
      [{"key":"A","value":"用户"},{"key":"B","value":"操作系统"},{"key":"C","value":"编译程序"},{"key":"D","value":"链接程序"}], "B", 303, 30, 'EASY')
add_q(2023, "UDP协议提供（ ）服务。",
      [{"key":"A","value":"面向连接的可靠"},{"key":"B","value":"无连接的不可靠"},{"key":"C","value":"面向连接的不可靠"},{"key":"D","value":"无连接的可靠"}], "B", 405, 40, 'EASY')
add_q(2023, "DNS协议使用的传输层协议是（ ）。",
      [{"key":"A","value":"TCP"},{"key":"B","value":"UDP"},{"key":"C","value":"ICMP"},{"key":"D","value":"HTTP"}], "B", 405, 40, 'EASY')
add_q(2023, "子网掩码为255.255.255.192，该子网可容纳的主机数为（ ）。",
      [{"key":"A","value":"64"},{"key":"B","value":"62"},{"key":"C","value":"128"},{"key":"D","value":"126"}], "B", 404, 40, 'MEDIUM')
add_q(2023, "CSMA/CD协议中，发生冲突后采用的退避算法是（ ）。",
      [{"key":"A","value":"线性退避"},{"key":"B","value":"截断二进制指数退避"},{"key":"C","value":"固定时间退避"},{"key":"D","value":"优先级退避"}], "B", 403, 40, 'EASY')

# ===== 2024 Choice Questions =====
add_q(2024, "在长度为n的顺序表中删除第i个元素(1<=i<=n)，需要向前移动（ ）个元素。",
      [{"key":"A","value":"i"},{"key":"B","value":"n-i"},{"key":"C","value":"n"},{"key":"D","value":"i-1"}], "B", 101, 10, 'EASY')
add_q(2024, "图的深度优先遍历类似于二叉树的（ ）。",
      [{"key":"A","value":"先序遍历"},{"key":"B","value":"中序遍历"},{"key":"C","value":"后序遍历"},{"key":"D","value":"层次遍历"}], "A", 104, 10, 'EASY')
add_q(2024, "下列排序算法中，不稳定的是（ ）。",
      [{"key":"A","value":"冒泡排序"},{"key":"B","value":"插入排序"},{"key":"C","value":"归并排序"},{"key":"D","value":"快速排序"}], "D", 106, 10, 'EASY')
add_q(2024, "AVL树是一种（ ）。",
      [{"key":"A","value":"二叉排序树"},{"key":"B","value":"平衡二叉排序树"},{"key":"C","value":"B树"},{"key":"D","value":"堆"}], "B", 103, 10, 'EASY')
add_q(2024, "Cache与主存之间的地址映射由（ ）完成。",
      [{"key":"A","value":"操作系统"},{"key":"B","value":"硬件"},{"key":"C","value":"用户程序"},{"key":"D","value":"编译器"}], "B", 203, 20, 'EASY')
add_q(2024, "某计算机字长32位，其存储容量为4GB，若按字编址，其寻址范围是（ ）。",
      [{"key":"A","value":"0~1G-1"},{"key":"B","value":"0~4G-1"},{"key":"C","value":"0~1GW-1"},{"key":"D","value":"0~4GW-1"}], "A", 201, 20, 'MEDIUM')
add_q(2024, "指令系统中采用不同的寻址方式的主要目的是（ ）。",
      [{"key":"A","value":"缩短指令长度，扩大寻址空间，提高编程灵活性"},{"key":"B","value":"增加指令条数"},{"key":"C","value":"简化电路设计"},{"key":"D","value":"提高指令执行速度"}], "A", 204, 20, 'EASY')
add_q(2024, "中断向量地址是（ ）。",
      [{"key":"A","value":"子程序入口地址"},{"key":"B","value":"中断服务程序的入口地址"},{"key":"C","value":"中断服务程序入口地址的地址"},{"key":"D","value":"中断返回地址"}], "C", 205, 20, 'MEDIUM')
add_q(2024, "操作系统中，信号量的值（ ）。",
      [{"key":"A","value":"只能是正整数"},{"key":"B","value":"只能是0或正整数"},{"key":"C","value":"可以是负整数"},{"key":"D","value":"不能为0"}], "C", 302, 30, 'EASY')
add_q(2024, "SPOOLing技术实现了（ ）。",
      [{"key":"A","value":"虚拟设备"},{"key":"B","value":"共享设备"},{"key":"C","value":"独占设备"},{"key":"D","value":"脱机设备"}], "A", 305, 30, 'MEDIUM')
add_q(2024, "文件系统中，文件存储空间管理常采用（ ）。",
      [{"key":"A","value":"页表"},{"key":"B","value":"段表"},{"key":"C","value":"位示图或空闲表"},{"key":"D","value":"快表"}], "C", 304, 30, 'EASY')
add_q(2024, "HTTP协议默认使用的端口号是（ ）。",
      [{"key":"A","value":"21"},{"key":"B","value":"25"},{"key":"C","value":"80"},{"key":"D","value":"110"}], "C", 405, 40, 'EASY')
add_q(2024, "TCP三次握手中，第二次握手发送的报文段是（ ）。",
      [{"key":"A","value":"SYN"},{"key":"B","value":"SYN+ACK"},{"key":"C","value":"ACK"},{"key":"D","value":"FIN"}], "B", 405, 40, 'EASY')
add_q(2024, "在OSI参考模型中，网络层的数据传输单位是（ ）。",
      [{"key":"A","value":"比特"},{"key":"B","value":"帧"},{"key":"C","value":"分组"},{"key":"D","value":"报文"}], "C", 401, 40, 'EASY')
add_q(2024, "ARP协议的功能是（ ）。",
      [{"key":"A","value":"将IP地址解析为MAC地址"},{"key":"B","value":"将MAC地址解析为IP地址"},{"key":"C","value":"将域名解析为IP地址"},{"key":"D","value":"将IP地址解析为域名"}], "A", 404, 40, 'EASY')

# ===== 2025 Choice Questions =====
add_q(2025, "一个栈的入栈序列是a,b,c,d,e，则栈的不可能的输出序列是（ ）。",
      [{"key":"A","value":"e,d,c,b,a"},{"key":"B","value":"d,e,c,b,a"},{"key":"C","value":"d,c,e,a,b"},{"key":"D","value":"a,b,c,d,e"}], "C", 102, 10, 'EASY')
add_q(2025, "下列数据结构中，属于非线性结构的是（ ）。",
      [{"key":"A","value":"栈"},{"key":"B","value":"队列"},{"key":"C","value":"二叉树"},{"key":"D","value":"线性表"}], "C", 103, 10, 'EASY')
add_q(2025, "对于长度为n的线性表，顺序查找的平均查找长度为（ ）。",
      [{"key":"A","value":"n/2"},{"key":"B","value":"(n+1)/2"},{"key":"C","value":"n"},{"key":"D","value":"logn"}], "B", 105, 10, 'EASY')
add_q(2025, "无向图G有16条边，3个度为4的顶点，其余顶点的度均不大于3，则G至少有（ ）个顶点。",
      [{"key":"A","value":"10"},{"key":"B","value":"11"},{"key":"C","value":"12"},{"key":"D","value":"13"}], "B", 104, 10, 'MEDIUM')
add_q(2025, "Cache的替换策略中，最近最少使用的是（ ）。",
      [{"key":"A","value":"FIFO"},{"key":"B","value":"LRU"},{"key":"C","value":"LFU"},{"key":"D","value":"Random"}], "B", 203, 20, 'EASY')
add_q(2025, "在计算机中，运算器的功能是（ ）。",
      [{"key":"A","value":"完成算术和逻辑运算"},{"key":"B","value":"存储数据"},{"key":"C","value":"控制指令执行"},{"key":"D","value":"传输数据"}], "A", 201, 20, 'EASY')
add_q(2025, "程序计数器PC属于（ ）。",
      [{"key":"A","value":"运算器"},{"key":"B","value":"控制器"},{"key":"C","value":"存储器"},{"key":"D","value":"I/O接口"}], "B", 205, 20, 'EASY')
add_q(2025, "浮点数的表示范围主要由（ ）决定。",
      [{"key":"A","value":"尾数的位数"},{"key":"B","value":"阶码的位数"},{"key":"C","value":"符号位的位数"},{"key":"D","value":"基数的选择"}], "B", 202, 20, 'EASY')
add_q(2025, "进程和程序的一个本质区别是（ ）。",
      [{"key":"A","value":"进程是动态的，程序是静态的"},{"key":"B","value":"进程存储在内存，程序存储在外存"},{"key":"C","value":"进程是顺序执行的，程序是并发执行的"},{"key":"D","value":"进程是持久的，程序是暂时的"}], "A", 301, 30, 'EASY')
add_q(2025, "虚拟存储器的最大容量由（ ）决定。",
      [{"key":"A","value":"内外存容量之和"},{"key":"B","value":"计算机的地址结构"},{"key":"C","value":"页表长度"},{"key":"D","value":"内存容量"}], "B", 303, 30, 'EASY')
add_q(2025, "在文件系统中，打开文件操作的主要功能是（ ）。",
      [{"key":"A","value":"把文件从外存调入内存"},{"key":"B","value":"把文件的FCB调入内存"},{"key":"C","value":"检查用户权限"},{"key":"D","value":"分配文件存储空间"}], "B", 304, 30, 'MEDIUM')
add_q(2025, "TCP协议中，拥塞控制不包括（ ）。",
      [{"key":"A","value":"慢启动"},{"key":"B","value":"拥塞避免"},{"key":"C","value":"快重传"},{"key":"D","value":"优先级调度"}], "D", 405, 40, 'MEDIUM')
add_q(2025, "以下属于应用层协议的是（ ）。",
      [{"key":"A","value":"IP"},{"key":"B","value":"TCP"},{"key":"C","value":"FTP"},{"key":"D","value":"ARP"}], "C", 405, 40, 'EASY')
add_q(2025, "RIP协议最大支持的跳数为（ ）。",
      [{"key":"A","value":"8"},{"key":"B","value":"15"},{"key":"C","value":"16"},{"key":"D","value":"32"}], "B", 404, 40, 'EASY')
add_q(2025, "在数据链路层，实现可靠传输的协议是（ ）。",
      [{"key":"A","value":"CSMA/CD"},{"key":"B","value":"HDLC"},{"key":"C","value":"IP"},{"key":"D","value":"UDP"}], "B", 403, 40, 'MEDIUM')

count = 0
for q in questions_extra:
    year, content, opts, ans, ch, subj, diff = q
    kp_id = get_kp(ch)
    cursor.execute(
        'INSERT INTO question (chapter_id, subject_id, type, difficulty, content, options, answer, year) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
        (ch, subj, 'SINGLE', diff, content, opts, ans, year)
    )
    qid = cursor.lastrowid
    if kp_id:
        cursor.execute('INSERT INTO question_knowledge (question_id, knowledge_id) VALUES (%s,%s)', (qid, kp_id))
    count += 1

conn.commit()
print(f'Inserted {count} new choice questions for 2022-2025')
cursor.close()
conn.close()