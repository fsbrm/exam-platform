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
        // Ensure schema migrations (safe idempotent ALTERs)
        try { jdbcTemplate.update("ALTER TABLE question ADD COLUMN video_url VARCHAR(500)"); } catch (Exception ignored) {}
        try { jdbcTemplate.update("ALTER TABLE user_answer ADD COLUMN IF NOT EXISTS answered_at DATETIME"); } catch (Exception ignored) {}

        // Check if seed is complete (chapters exist = fully seeded)
        try {
            Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM chapter", Integer.class);
            if (count != null && count > 0) {
                log.info("Data already seeded: {} chapters exist, skipping", count);
                return;
            }
        } catch (Exception e) {
            log.info("Chapter table not ready, will seed data...");
        }

        try {
            // Clean any partial data from previous failed seed attempts
            log.info("Cleaning partial data...");
            jdbcTemplate.update("DELETE FROM question_knowledge");
            jdbcTemplate.update("DELETE FROM paper_question");
            jdbcTemplate.update("DELETE FROM question");
            jdbcTemplate.update("DELETE FROM knowledge_point");
            jdbcTemplate.update("DELETE FROM exam_paper");
            jdbcTemplate.update("DELETE FROM chapter");
            log.info("Partial data cleaned, loading seed...");

            ClassPathResource resource = new ClassPathResource("railway-seed.sql");
            String sql = StreamUtils.copyToString(resource.getInputStream(), StandardCharsets.UTF_8);

            // Split by INSERT IGNORE statements and execute each
            String[] statements = sql.split("(?=INSERT IGNORE)");
            int executed = 0;
            int failed = 0;
            for (String stmt : statements) {
                String trimmed = stmt.trim();
                if (trimmed.isEmpty()) continue;
                try {
                    jdbcTemplate.update(trimmed);
                    executed++;
                } catch (Exception ex) {
                    failed++;
                    String err = ex.getMessage();
                    log.warn("Seed error #{}: {} | SQL start: {}...",
                            failed,
                            err != null ? err.substring(0, Math.min(150, err.length())) : "null",
                            trimmed.substring(0, Math.min(100, trimmed.length())));
                }
            }
            log.info("Seed complete: {} executed, {} failed", executed, failed);
        } catch (Exception e) {
            log.error("Seeding failed: {}", e.getMessage(), e);
        }
    }
}
