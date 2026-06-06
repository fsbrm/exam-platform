package com.exam.controller;

import com.exam.common.Result;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.DashboardService;
import java.util.HashMap;
import java.util.Map;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@Tag(name = "学习数据分析接口")
@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;

    @Operation(summary = "个人仪表盘总览")
    @GetMapping
    public Result<?> dashboard() {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(dashboardService.getUserDashboard(userId));
    }

    @Operation(summary = "科目分析")
    @GetMapping("/subject/{subjectId}")
    public Result<?> subjectAnalytics(@PathVariable Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(dashboardService.getSubjectAnalytics(userId, subjectId));
    }

    @Operation(summary = "周统计")
    @GetMapping("/weekly")
    public Result<?> weekly() {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(dashboardService.getWeeklyStats(userId));
    }

    @Operation(summary = "年度热力图数据（日期→刷题数）")
    @GetMapping("/heatmap")
    public Result<?> heatmap() {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        Map<String, Object> result = new HashMap<>();
        result.put("data", dashboardService.getHeatmapData(userId));
        return Result.success(result);
    }

    @Operation(summary = "科目首页面板数据（未登录返回空数据）")
    @GetMapping("/subject/{subjectId}/panel")
    public Result<?> subjectPanel(@PathVariable Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.success(dashboardService.emptySubjectPanel());
        return Result.success(dashboardService.getSubjectPanel(userId, subjectId));
    }
}