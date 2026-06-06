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