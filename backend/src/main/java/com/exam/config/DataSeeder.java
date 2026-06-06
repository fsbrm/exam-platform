package com.exam.config;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import org.springframework.util.StreamUtils;

import java.nio.charset.StandardCharsets;

@Slf4j
@Component
@RequiredArgsConstructor
public class DataSeeder implements CommandLineRunner {

    private final JdbcTemplate jdbcTemplate;

    @Override
    public void run(String... args) {
        try {
            // Check if data already exists
            Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM question", Integer.class);
            if (count != null && count > 0) {
                log.info("Data already seeded: {} questions exist, skipping", count);
                return;
            }
        } catch (Exception e) {
            log.info("Question table not found, will seed data...");
        }

        try {
            log.info("Loading seed data from railway-seed.sql...");
            ClassPathResource resource = new ClassPathResource("railway-seed.sql");
            String sql = StreamUtils.copyToString(resource.getInputStream(), StandardCharsets.UTF_8);

            // Split by INSERT statements and execute in batches
            String[] statements = sql.split("(?=INSERT IGNORE)");
            int executed = 0;
            for (String stmt : statements) {
                String trimmed = stmt.trim();
                if (trimmed.isEmpty()) continue;
                try {
                    jdbcTemplate.execute(trimmed);
                    executed++;
                } catch (Exception ex) {
                    log.warn("Skipping statement: {}", ex.getMessage().substring(0, Math.min(100, ex.getMessage().length())));
                }
            }
            log.info("Seed complete: {} statements executed", executed);
        } catch (Exception e) {
            log.error("Seeding failed: {}", e.getMessage());
        }
    }
}