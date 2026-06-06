-- =============================================
-- 408真题刷题平台 - 数据库重构 v2.0
-- =============================================
CREATE DATABASE IF NOT EXISTS exam_platform DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
USE exam_platform;

DROP TABLE IF EXISTS question_knowledge;
DROP TABLE IF EXISTS paper_question;
DROP TABLE IF EXISTS exam_paper;
DROP TABLE IF EXISTS knowledge_point;
DROP TABLE IF EXISTS user_answer;
DROP TABLE IF EXISTS exam_question;
DROP TABLE IF EXISTS exam_record;
DROP TABLE IF EXISTS wrong_question;
DROP TABLE IF EXISTS favorite;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS chapter;
DROP TABLE IF EXISTS subject;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    nickname VARCHAR(50),
    avatar VARCHAR(255),
    role VARCHAR(20) DEFAULT 'USER',
    status TINYINT DEFAULT 1,
    image VARCHAR(500) COMMENT '题目配图路径',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted TINYINT DEFAULT 0
) COMMENT '用户表';

CREATE TABLE subject (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    icon VARCHAR(50),
    sort_order INT DEFAULT 0,
    status TINYINT DEFAULT 1,
    image VARCHAR(500) COMMENT '题目配图路径',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) COMMENT '科目表';

CREATE TABLE chapter (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    subject_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    parent_id BIGINT DEFAULT 0,
    sort_order INT DEFAULT 0,
    question_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) COMMENT '章节表';

CREATE TABLE knowledge_point (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    subject_id BIGINT NOT NULL,
    chapter_id BIGINT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_id BIGINT DEFAULT 0,
    level INT DEFAULT 1,
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) COMMENT '知识点表';

CREATE TABLE exam_paper (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    subject_id BIGINT NOT NULL,
    year INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    total_score INT DEFAULT 150,
    duration INT DEFAULT 180,
    question_count INT DEFAULT 47,
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_subject_year (subject_id, year)
) COMMENT '真题试卷表';

CREATE TABLE paper_question (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    paper_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    question_number INT,
    score INT DEFAULT 2,
    sort_order INT DEFAULT 0,
    UNIQUE KEY uk_paper_question (paper_id, question_id)
) COMMENT '试卷题目关联表';

CREATE TABLE question_knowledge (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    question_id BIGINT NOT NULL,
    knowledge_id BIGINT NOT NULL,
    UNIQUE KEY uk_qk (question_id, knowledge_id)
) COMMENT '题目知识点关联表';

CREATE TABLE question (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    chapter_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    type VARCHAR(20) NOT NULL,
    difficulty VARCHAR(10) DEFAULT 'MEDIUM',
    content TEXT NOT NULL,
    options JSON,
    answer VARCHAR(500) NOT NULL,
    analysis TEXT,
    year INT,
    status TINYINT DEFAULT 1,
    image VARCHAR(500) COMMENT '题目配图路径',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '题目表';

CREATE TABLE user_answer (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    user_answer VARCHAR(500),
    is_correct TINYINT,
    time_taken INT DEFAULT 0,
    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_subject (user_id, subject_id),
    INDEX idx_user_time (user_id, answered_at)
) COMMENT '答题记录表';

CREATE TABLE exam_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    total_questions INT NOT NULL,
    correct_count INT DEFAULT 0,
    score DECIMAL(5,1) DEFAULT 0,
    duration INT,
    time_limit INT NOT NULL,
    status VARCHAR(20) DEFAULT 'IN_PROGRESS',
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME,
    INDEX idx_user_exam (user_id, subject_id)
) COMMENT '考试记录表';

CREATE TABLE exam_question (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    exam_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    user_answer VARCHAR(500),
    is_correct TINYINT,
    sort_order INT DEFAULT 0
) COMMENT '考试题目关联表';

CREATE TABLE wrong_question (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    subject_id BIGINT NOT NULL,
    wrong_count INT DEFAULT 1,
    last_wrong_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_removed TINYINT DEFAULT 0,
    UNIQUE KEY uk_user_question (user_id, question_id)
) COMMENT '错题本表';

CREATE TABLE favorite (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_question (user_id, question_id)
) COMMENT '收藏表';

CREATE TABLE note (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    question_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '笔记表';

-- ============ 初始数据 ============
INSERT INTO subject (id, name, description, icon, sort_order) VALUES
(1, '408 计算机综合', '数据结构·计算机组成原理·操作系统·计算机网络', 'computer', 1);

INSERT INTO user (username, password, email, nickname, role) VALUES
('admin', '.eOki5S/P9OWG2E4m2.20LpQ6kXaOwU2LJ2A.eq/lEMnotqIfO', 'admin@exam.com', '管理员', 'ADMIN');

-- 章节
INSERT INTO chapter (id, subject_id, name, parent_id, sort_order) VALUES
(1, 1, '数据结构', 0, 1),(2, 1, '计算机组成原理', 0, 2),
(3, 1, '操作系统', 0, 3),(4, 1, '计算机网络', 0, 4);

INSERT INTO chapter (id, subject_id, name, parent_id, sort_order) VALUES
(5,1,'线性表',1,1),(6,1,'栈与队列',1,2),(7,1,'树与二叉树',1,3),
(8,1,'图',1,4),(9,1,'查找',1,5),(10,1,'排序',1,6),
(11,1,'数据表示与运算',2,1),(12,1,'存储系统',2,2),(13,1,'指令系统',2,3),
(14,1,'中央处理器',2,4),(15,1,'总线与I/O',2,5),
(16,1,'进程管理',3,1),(17,1,'内存管理',3,2),(18,1,'文件管理',3,3),(19,1,'I/O管理',3,4),
(20,1,'计算机网络体系结构',4,1),(21,1,'物理层',4,2),(22,1,'数据链路层',4,3),
(23,1,'网络层',4,4),(24,1,'传输层',4,5),(25,1,'应用层',4,6);

-- 知识点 (55个)
INSERT INTO knowledge_point (id, subject_id, chapter_id, name, parent_id, level, sort_order) VALUES
(1,1,5,'顺序表',0,1,1),(2,1,5,'链表',0,1,2),
(3,1,6,'栈',0,1,1),(4,1,6,'队列',0,1,2),(5,1,6,'表达式求值',0,1,3),
(6,1,7,'二叉树性质与遍历',0,1,1),(7,1,7,'二叉搜索树',0,1,2),(8,1,7,'平衡二叉树',0,1,3),
(9,1,7,'哈夫曼树',0,1,4),(10,1,7,'树的应用',0,1,5),
(11,1,8,'图的存储与遍历',0,1,1),(12,1,8,'最小生成树',0,1,2),(13,1,8,'最短路径',0,1,3),
(14,1,8,'拓扑排序与关键路径',0,1,4),
(15,1,9,'顺序查找与二分查找',0,1,1),(16,1,9,'散列表',0,1,2),(17,1,9,'B树与B+树',0,1,3),
(18,1,10,'插入与交换排序',0,1,1),(19,1,10,'选择与归并排序',0,1,2),(20,1,10,'外部排序',0,1,3),
(21,1,11,'数制与编码',0,1,1),(22,1,11,'定点与浮点运算',0,1,2),
(23,1,12,'Cache',0,1,1),(24,1,12,'虚拟存储器',0,1,2),(25,1,12,'主存储器',0,1,3),
(26,1,13,'指令格式与寻址',0,1,1),(27,1,13,'CISC与RISC',0,1,2),
(28,1,14,'CPU结构与数据通路',0,1,1),(29,1,14,'指令流水线',0,1,2),
(30,1,15,'总线',0,1,1),(31,1,15,'I/O方式',0,1,2),
(32,1,16,'进程与线程',0,1,1),(33,1,16,'进程同步与互斥',0,1,2),(34,1,16,'死锁',0,1,3),
(35,1,16,'处理机调度',0,1,4),
(36,1,17,'连续分配与分页',0,1,1),(37,1,17,'页面置换算法',0,1,2),(38,1,17,'分段与段页式',0,1,3),
(39,1,18,'文件系统基础',0,1,1),(40,1,18,'文件存储与保护',0,1,2),
(41,1,19,'磁盘调度',0,1,1),(42,1,19,'I/O控制与SPOOLing',0,1,2),
(43,1,20,'OSI与TCP/IP模型',0,1,1),
(44,1,21,'编码与传输介质',0,1,1),
(45,1,22,'差错控制与流量控制',0,1,1),(46,1,22,'CSMA与以太网',0,1,2),
(47,1,23,'IPv4与子网划分',0,1,1),(48,1,23,'路由协议',0,1,2),(49,1,23,'IPv6',0,1,3),
(50,1,24,'TCP可靠传输',0,1,1),(51,1,24,'TCP拥塞控制',0,1,2),(52,1,24,'UDP',0,1,3),
(53,1,25,'DNS与HTTP',0,1,1),(54,1,25,'FTP与电子邮件',0,1,2),(55,1,25,'网络安全基础',0,1,3);

-- 真题试卷 2009-2026 (18年)INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (1, 1, 2009, '2009年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (2, 1, 2010, '2010年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (3, 1, 2011, '2011年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (4, 1, 2012, '2012年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (5, 1, 2013, '2013年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (6, 1, 2014, '2014年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (7, 1, 2015, '2015年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (8, 1, 2016, '2016年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (9, 1, 2017, '2017年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (10, 1, 2018, '2018年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (11, 1, 2019, '2019年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (12, 1, 2020, '2020年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (13, 1, 2021, '2021年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (14, 1, 2022, '2022年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (15, 1, 2023, '2023年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (16, 1, 2024, '2024年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (17, 1, 2025, '2025年408计算机综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (18, 1, 2026, '2026年408计算机综合真题', 150, 180, 47);
