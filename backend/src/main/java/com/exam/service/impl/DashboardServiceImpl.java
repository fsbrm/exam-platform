package com.exam.service.impl;

import com.exam.mapper.UserAnswerMapper;
import com.exam.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

@Service
@RequiredArgsConstructor
public class DashboardServiceImpl implements DashboardService {

    private final UserAnswerMapper userAnswerMapper;

    @Override
    public Map<String, Object> getUserDashboard(Long userId) {
        Map<String, Object> result = new HashMap<>();

        Long totalQuestions = userAnswerMapper.countByUser(userId);
        Long correctQuestions = userAnswerMapper.countCorrectByUser(userId);
        Integer studyDays = userAnswerMapper.countStudyDays(userId);

        BigDecimal accuracy = BigDecimal.ZERO;
        if (totalQuestions > 0) {
            accuracy = BigDecimal.valueOf((double) correctQuestions / totalQuestions * 100)
                    .setScale(1, RoundingMode.HALF_UP);
        }

        // 连续打卡天数
        int streakDays = calculateStreak(userId);

        Map<String, Object> overview = new HashMap<>();
        overview.put("totalQuestions", totalQuestions);
        overview.put("correctQuestions", correctQuestions);
        overview.put("accuracy", accuracy);
        overview.put("studyDays", studyDays);
        overview.put("streakDays", streakDays);
        result.put("overview", overview);

        // 今日统计
        Long todayCountVal = userAnswerMapper.countTodayByUser(userId);
        Long todayCorrectVal = userAnswerMapper.countTodayCorrectByUser(userId);
        result.put("todayCount", todayCountVal != null ? todayCountVal : 0L);
        result.put("todayCorrect", todayCorrectVal != null ? todayCorrectVal : 0L);

        // 热力图数据（近一年每日刷题数）
        List<Map<String, Object>> heatmapList = userAnswerMapper.dailyCount(userId, LocalDate.now().minusDays(365));
        Map<String, Integer> heatmap = new LinkedHashMap<>();
        for (Map<String, Object> row : heatmapList) {
            Object dateObj = row.get("date");
            Object countObj = row.get("count");
            String dateStr = null;
            if (dateObj instanceof java.sql.Date) {
                dateStr = ((java.sql.Date) dateObj).toLocalDate().toString();
            } else if (dateObj instanceof LocalDate) {
                dateStr = ((LocalDate) dateObj).toString();
            } else if (dateObj != null) {
                dateStr = dateObj.toString();
            }
            Integer count = 0;
            if (countObj instanceof Number) {
                count = ((Number) countObj).intValue();
            }
            if (dateStr != null) {
                heatmap.put(dateStr, count);
            }
        }
        result.put("heatmap", heatmap);

        // 科目统计
        List<Map<String, Object>> subjectStats = userAnswerMapper.subjectStats(userId);
        result.put("subjectStats", subjectStats);

        return result;
    }

    @Override
    public Map<String, Object> getSubjectAnalytics(Long userId, Long subjectId) {
        Map<String, Object> result = new HashMap<>();

        // 每日刷题趋势 (最近30天)
        LocalDate startDate = LocalDate.now().minusDays(30);
        List<Map<String, Object>> dailyStats = userAnswerMapper.dailyStats(userId, startDate);
        result.put("dailyStats", dailyStats);

        return result;
    }

    @Override
    public Map<String, Object> getWeeklyStats(Long userId) {
        Map<String, Object> result = new HashMap<>();
        LocalDate startDate = LocalDate.now().minusDays(7);
        List<Map<String, Object>> dailyStats = userAnswerMapper.dailyStats(userId, startDate);
        result.put("dailyStats", dailyStats);
        return result;
    }

    private int calculateStreak(Long userId) {
        // 简单的连续打卡计算：从今天往回数
        int streak = 0;
        LocalDate today = LocalDate.now();
        List<Map<String, Object>> dailyCounts = userAnswerMapper.dailyCount(userId, today.minusDays(365));
        Set<LocalDate> activeDates = new HashSet<>();
        for (Map<String, Object> dc : dailyCounts) {
            if (dc.get("date") instanceof java.sql.Date) {
                activeDates.add(((java.sql.Date) dc.get("date")).toLocalDate());
            } else if (dc.get("date") instanceof LocalDate) {
                activeDates.add((LocalDate) dc.get("date"));
            }
        }

        LocalDate check = today;
        while (activeDates.contains(check)) {
            streak++;
            check = check.minusDays(1);
        }
        return streak;
    }

    @Override
    public Map<String, Object> getSubjectPanel(Long userId, Long subjectId) {
        Map<String, Object> result = new HashMap<>();

        // Subject overview stats
        Long totalQuestions = userAnswerMapper.countByUserAndSubject(userId, subjectId);
        Long correctQuestions = userAnswerMapper.countCorrectByUserAndSubject(userId, subjectId);
        Integer studyDays = userAnswerMapper.countStudyDaysBySubject(userId, subjectId);

        BigDecimal accuracy = BigDecimal.ZERO;
        if (totalQuestions > 0) {
            accuracy = BigDecimal.valueOf((double) correctQuestions / totalQuestions * 100)
                    .setScale(1, RoundingMode.HALF_UP);
        }

        // Streak for this subject
        int streakDays = calculateSubjectStreak(userId, subjectId);

        Map<String, Object> overview = new HashMap<>();
        overview.put("totalDone", totalQuestions);
        overview.put("correctCount", correctQuestions);
        overview.put("accuracy", accuracy);
        overview.put("studyDays", studyDays);
        overview.put("streakDays", streakDays);
        result.put("overview", overview);

        // Recent 7-day activity
        LocalDate weekStart = LocalDate.now().minusDays(6);
        List<Map<String, Object>> dailyStats = userAnswerMapper.dailyStatsBySubject(userId, subjectId, weekStart);
        result.put("dailyActivity", dailyStats);

        // Chapter mastery
        List<Map<String, Object>> chapterMastery = userAnswerMapper.chapterMasteryBySubject(userId, subjectId);
        result.put("chapterMastery", chapterMastery);

        return result;
    }

    @Override
    public List<Map<String, Object>> getHeatmapData(Long userId) {
        LocalDate startDate = LocalDate.now().minusDays(365);
        return userAnswerMapper.dailyCount(userId, startDate);
    }

    @Override
    public Map<String, Object> emptySubjectPanel() {
        Map<String, Object> result = new HashMap<>();
        Map<String, Object> overview = new HashMap<>();
        overview.put("totalDone", 0L);
        overview.put("correctCount", 0L);
        overview.put("accuracy", BigDecimal.ZERO);
        overview.put("studyDays", 0);
        overview.put("streakDays", 0);
        result.put("overview", overview);
        result.put("dailyActivity", new ArrayList<>());
        result.put("chapterMastery", new ArrayList<>());
        return result;
    }

    private int calculateSubjectStreak(Long userId, Long subjectId) {
        int streak = 0;
        LocalDate today = LocalDate.now();
        List<Map<String, Object>> dailyCounts = userAnswerMapper.dailyCountBySubject(userId, subjectId, today.minusDays(365));
        Set<LocalDate> activeDates = new HashSet<>();
        for (Map<String, Object> dc : dailyCounts) {
            if (dc.get("date") instanceof java.sql.Date) {
                activeDates.add(((java.sql.Date) dc.get("date")).toLocalDate());
            }
        }

        LocalDate check = today;
        while (activeDates.contains(check)) {
            streak++;
            check = check.minusDays(1);
        }
        return streak;
    }
}