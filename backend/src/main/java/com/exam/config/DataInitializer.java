package com.exam.config;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.entity.User;
import com.exam.mapper.UserMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;
    private final JdbcTemplate jdbcTemplate;

    @Override
    public void run(String... args) {
        initInviteCodeTable();
        initAdminUser();
    }

    private void initInviteCodeTable() {
        try {
            jdbcTemplate.execute(
                "CREATE TABLE IF NOT EXISTS invite_code (" +
                "id BIGINT AUTO_INCREMENT PRIMARY KEY, " +
                "code VARCHAR(32) NOT NULL UNIQUE, " +
                "used TINYINT DEFAULT 0, " +
                "used_by BIGINT DEFAULT NULL, " +
                "used_at DATETIME DEFAULT NULL, " +
                "created_at DATETIME DEFAULT CURRENT_TIMESTAMP, " +
                "created_by BIGINT DEFAULT NULL, " +
                "INDEX idx_code (code), " +
                "INDEX idx_used (used)" +
                ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
            );
            log.info("invite_code table ready");
        } catch (Exception e) {
            log.warn("invite_code table init skipped: {}", e.getMessage());
        }
    }

    private void initAdminUser() {
        User admin = userMapper.selectOne(
            new LambdaQueryWrapper<User>().eq(User::getUsername, "admin")
        );
        if (admin == null) {
            admin = new User();
            admin.setUsername("admin");
            admin.setPassword(passwordEncoder.encode("cxy0721"));
            admin.setNickname("管理员");
            admin.setRole("ADMIN");
            admin.setStatus(1);
            userMapper.insert(admin);
            log.info("Admin user created: admin / cxy0721");
        } else {
            // Ensure password is proper BCrypt
            String pwd = admin.getPassword();
            if (pwd == null || !pwd.startsWith("$2a$")) {
                admin.setPassword(passwordEncoder.encode("cxy0721"));
                userMapper.updateById(admin);
                log.info("Admin password reset to BCrypt hash");
            }
        }
    }
}