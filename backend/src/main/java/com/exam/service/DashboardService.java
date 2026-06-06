package com.exam.service;

import java.util.List;
import java.util.Map;

public interface DashboardService {
    Map<String, Object> getUserDashboard(Long userId);
    Map<String, Object> getSubjectAnalytics(Long userId, Long subjectId);
    Map<String, Object> getWeeklyStats(Long userId);
    Map<String, Object> getSubjectPanel(Long userId, Long subjectId);
    List<Map<String, Object>> getHeatmapData(Long userId);
    Map<String, Object> emptySubjectPanel();
}