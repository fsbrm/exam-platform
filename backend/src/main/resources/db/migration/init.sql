-- =============================================
-- 智能备考与学习数据分析平台 - 数据库初始化
-- =============================================

CREATE DATABASE IF NOT EXISTS exam_platform
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE exam_platform;

-- 用户表
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码(BCrypt加密)',
    email VARCHAR(100) COMMENT '邮箱',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar VARCHAR(255) COMMENT '头像URL',
    role VARCHAR(20) DEFAULT 'USER' COMMENT '角色: USER/ADMIN',
    status TINYINT DEFAULT 1 COMMENT '状态: 1正常 0禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted TINYINT DEFAULT 0 COMMENT '逻辑删除'
) COMMENT '用户表';

-- 科目表
DROP TABLE IF EXISTS subject;
CREATE TABLE subject (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '科目名称',
    description VARCHAR(255) COMMENT '科目描述',
    icon VARCHAR(50) COMMENT '图标',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) COMMENT '科目表';

-- 章节表
DROP TABLE IF EXISTS chapter;
CREATE TABLE chapter (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    subject_id BIGINT NOT NULL COMMENT '科目ID',
    name VARCHAR(100) NOT NULL COMMENT '章节名称',
    description VARCHAR(255) COMMENT '章节描述',
    parent_id BIGINT DEFAULT 0 COMMENT '父章节ID(0=顶级)',
    sort_order INT DEFAULT 0 COMMENT '排序',
    question_count INT DEFAULT 0 COMMENT '题目数量(冗余)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) COMMENT '章节表';

-- 题目表
DROP TABLE IF EXISTS question;
CREATE TABLE question (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    chapter_id BIGINT NOT NULL COMMENT '章节ID',
    subject_id BIGINT NOT NULL COMMENT '科目ID',
    type VARCHAR(20) NOT NULL COMMENT '题型: SINGLE/MULTI/JUDGE/FILL',
    difficulty VARCHAR(10) DEFAULT 'MEDIUM' COMMENT '难度: EASY/MEDIUM/HARD',
    content TEXT NOT NULL COMMENT '题目内容',
    options JSON COMMENT '选项JSON: [{"key":"A","value":"..."}]',
    answer VARCHAR(500) NOT NULL COMMENT '正确答案',
    analysis TEXT COMMENT '解析',
    status TINYINT DEFAULT 1 COMMENT '状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '题目表';

-- 答题记录表
DROP TABLE IF EXISTS user_answer;
CREATE TABLE user_answer (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    question_id BIGINT NOT NULL COMMENT '题目ID',
    subject_id BIGINT NOT NULL COMMENT '科目ID',
    user_answer VARCHAR(500) COMMENT '用户答案',
    is_correct TINYINT COMMENT '是否正确: 1正确 0错误',
    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_subject (user_id, subject_id),
    INDEX idx_user_time (user_id, answered_at)
) COMMENT '答题记录表';

-- 考试记录表
DROP TABLE IF EXISTS exam_record;
CREATE TABLE exam_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    subject_id BIGINT NOT NULL COMMENT '科目ID',
    total_questions INT NOT NULL COMMENT '总题数',
    correct_count INT DEFAULT 0 COMMENT '正确数',
    score DECIMAL(5,1) DEFAULT 0 COMMENT '得分',
    duration INT COMMENT '考试时长(秒)',
    time_limit INT NOT NULL COMMENT '限时(分钟)',
    status VARCHAR(20) DEFAULT 'IN_PROGRESS' COMMENT '状态: IN_PROGRESS/FINISHED/TIMEOUT',
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME,
    INDEX idx_user_exam (user_id, subject_id)
) COMMENT '考试记录表';

-- 考试题目关联表
DROP TABLE IF EXISTS exam_question;
CREATE TABLE exam_question (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    exam_id BIGINT NOT NULL COMMENT '考试ID',
    question_id BIGINT NOT NULL COMMENT '题目ID',
    user_answer VARCHAR(500) COMMENT '用户答案',
    is_correct TINYINT COMMENT '是否正确',
    sort_order INT DEFAULT 0 COMMENT '题目顺序'
) COMMENT '考试题目关联表';

-- 错题本表
DROP TABLE IF EXISTS wrong_question;
CREATE TABLE wrong_question (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    question_id BIGINT NOT NULL COMMENT '题目ID',
    subject_id BIGINT NOT NULL COMMENT '科目ID',
    wrong_count INT DEFAULT 1 COMMENT '错误次数',
    last_wrong_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '最后错误时间',
    is_removed TINYINT DEFAULT 0 COMMENT '是否移除(做对后标记)',
    UNIQUE KEY uk_user_question (user_id, question_id)
) COMMENT '错题本表';

-- 收藏表
DROP TABLE IF EXISTS favorite;
CREATE TABLE favorite (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    question_id BIGINT NOT NULL COMMENT '题目ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_question (user_id, question_id)
) COMMENT '收藏表';

-- 笔记表
DROP TABLE IF EXISTS note;
CREATE TABLE note (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL COMMENT '用户ID',
    question_id BIGINT NOT NULL COMMENT '题目ID',
    content TEXT NOT NULL COMMENT '笔记内容',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '笔记表';

-- =============================================
-- 初始数据：科目
-- =============================================
INSERT INTO subject (name, description, icon, sort_order) VALUES
('408 计算机综合', '数据结构、计算机组成原理、操作系统、计算机网络', 'computer', 1),
('高等数学', '函数极限、微积分、微分方程、无穷级数', 'math', 2);

-- =============================================
-- 初始数据：章节 (408)
-- =============================================
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
-- 408 章节
(1, '数据结构', NULL, 0, 1),
(1, '计算机组成原理', NULL, 0, 2),
(1, '操作系统', NULL, 0, 3),
(1, '计算机网络', NULL, 0, 4);

-- 数据结构子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(1, '线性表', NULL, 1, 1),
(1, '栈与队列', NULL, 1, 2),
(1, '树与二叉树', NULL, 1, 3),
(1, '图', NULL, 1, 4),
(1, '查找', NULL, 1, 5),
(1, '排序', NULL, 1, 6);

-- 计组子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(1, '数据表示与运算', NULL, 2, 1),
(1, '存储系统', NULL, 2, 2),
(1, '指令系统', NULL, 2, 3),
(1, '中央处理器', NULL, 2, 4),
(1, '总线与I/O', NULL, 2, 5);

-- 操作系统子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(1, '进程管理', NULL, 3, 1),
(1, '内存管理', NULL, 3, 2),
(1, '文件管理', NULL, 3, 3),
(1, 'I/O管理', NULL, 3, 4);

-- 计网子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(1, '计算机网络体系结构', NULL, 4, 1),
(1, '物理层', NULL, 4, 2),
(1, '数据链路层', NULL, 4, 3),
(1, '网络层', NULL, 4, 4),
(1, '传输层', NULL, 4, 5),
(1, '应用层', NULL, 4, 6);

-- =============================================
-- 初始数据：章节 (高数)
-- =============================================
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
-- 高数父章节
(2, '函数与极限', NULL, 0, 1),
(2, '一元函数微分学', NULL, 0, 2),
(2, '一元函数积分学', NULL, 0, 3),
(2, '多元函数微分学', NULL, 0, 4),
(2, '多元函数积分学', NULL, 0, 5),
(2, '微分方程', NULL, 0, 6),
(2, '无穷级数', NULL, 0, 7);

-- 函数与极限子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(2, '函数的概念与性质', NULL, 25, 1),
(2, '极限与连续', NULL, 25, 2);

-- 一元微分子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(2, '导数与微分', NULL, 26, 1),
(2, '微分中值定理', NULL, 26, 2),
(2, '导数应用', NULL, 26, 3);

-- 一元积分子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(2, '不定积分', NULL, 27, 1),
(2, '定积分', NULL, 27, 2),
(2, '定积分应用', NULL, 27, 3);

-- 多元微分子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(2, '多元函数微分法', NULL, 28, 1),
(2, '多元函数极值', NULL, 28, 2);

-- 多元积分子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(2, '二重积分', NULL, 29, 1),
(2, '三重积分', NULL, 29, 2),
(2, '曲线与曲面积分', NULL, 29, 3);

-- 微分方程子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(2, '一阶微分方程', NULL, 30, 1),
(2, '高阶微分方程', NULL, 30, 2);

-- 无穷级数子章节
INSERT INTO chapter (subject_id, name, description, parent_id, sort_order) VALUES
(2, '常数项级数', NULL, 31, 1),
(2, '幂级数', NULL, 31, 2),
(2, '傅里叶级数', NULL, 31, 3);

-- 管理员账号 (admin / 123456)
INSERT INTO user (username, password, email, nickname, role) VALUES
('admin', '$2a$10$jkP.eOki5S/P9OWG2E4m2.20LpQ6kXaOwU2LJ2A.eq/lEMnotqIfO', 'admin@exam.com', '管理员', 'ADMIN');
