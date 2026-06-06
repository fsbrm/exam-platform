-- Invite code table
CREATE TABLE IF NOT EXISTS invite_code (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(32) NOT NULL UNIQUE,
    used TINYINT DEFAULT 0,
    used_by BIGINT DEFAULT NULL,
    used_at DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT DEFAULT NULL,
    INDEX idx_code (code),
    INDEX idx_used (used)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO subject (id, name, description, icon, sort_order, status) VALUES
(1, '数据结构', '408计算机统考-数据结构', 'Monitor', 1, 1),
(2, '计算机组成原理', '408计算机统考-计算机组成原理', 'Cpu', 2, 1),
(3, '操作系统', '408计算机统考-操作系统', 'Operation', 3, 1),
(4, '计算机网络', '408计算机统考-计算机网络', 'Connection', 4, 1);