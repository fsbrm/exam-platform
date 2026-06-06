package com.exam.controller;

import com.exam.common.Result;
import com.exam.security.JwtUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.Statement;
import java.util.LinkedHashMap;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class HealthController {

    private final DataSource dataSource;
    private final RedisConnectionFactory redisConnectionFactory;
    private final JwtUtils jwtUtils;

    @GetMapping("/health")
    public Result<Map<String, Object>> health() {
        Map<String, Object> checks = new LinkedHashMap<>();
        boolean allUp = true;

        // 1. Database check
        try (Connection conn = dataSource.getConnection();
             Statement stmt = conn.createStatement()) {
            stmt.execute("SELECT 1");
            checks.put("database", "OK");
        } catch (Exception e) {
            checks.put("database", "FAIL: " + e.getMessage());
            allUp = false;
            log.error("Health check - DB failed", e);
        }

        // 2. Redis check
        try {
            String pong = redisConnectionFactory.getConnection().ping();
            checks.put("redis", pong != null ? "OK" : "FAIL: no pong");
            if (pong == null) allUp = false;
        } catch (Exception e) {
            checks.put("redis", "FAIL: " + e.getMessage());
            allUp = false;
            log.error("Health check - Redis failed", e);
        }

        // 3. JWT check (generate + validate a test token)
        try {
            String testToken = jwtUtils.generateToken(0L, "health-check", "TEST");
            boolean valid = jwtUtils.validateToken(testToken);
            checks.put("jwt", valid ? "OK" : "FAIL: token validation returned false");
            if (!valid) allUp = false;
        } catch (Exception e) {
            checks.put("jwt", "FAIL: " + e.getClass().getSimpleName() + " - " + e.getMessage());
            allUp = false;
            log.error("Health check - JWT failed", e);
        }

        checks.put("status", allUp ? "UP" : "DEGRADED");
        return Result.success(checks);
    }
}
