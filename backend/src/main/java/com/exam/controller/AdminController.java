package com.exam.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.exam.common.BusinessException;
import com.exam.common.Result;
import com.exam.dto.QuestionQueryDTO;
import com.exam.entity.*;
import com.exam.mapper.*;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.DashboardService;
import com.exam.service.QuestionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Tag(name = "管理后台接口")
@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {

    private final QuestionService questionService;
    private final QuestionMapper questionMapper;
    private final DashboardService dashboardService;
    private final InviteCodeMapper inviteCodeMapper;
    private final UserMapper userMapper;
    private final UserAnswerMapper userAnswerMapper;
    private final SubjectMapper subjectMapper;

    // ==================== Question Management ====================

    @Operation(summary = "题目列表")
    @GetMapping("/questions")
    public Result<?> questions(QuestionQueryDTO dto) {
        return Result.success(questionService.pageQuery(dto));
    }

    @Operation(summary = "新增题目")
    @PostMapping("/questions")
    public Result<?> addQuestion(@RequestBody Question question) {
        if (question.getStatus() == null) question.setStatus(1);
        question.setCreatedAt(LocalDateTime.now());
        question.setUpdatedAt(LocalDateTime.now());
        questionMapper.insert(question);
        return Result.success(question);
    }

    @Operation(summary = "更新题目")
    @PutMapping("/questions/{id}")
    public Result<?> updateQuestion(@PathVariable Long id, @RequestBody Question question) {
        question.setId(id);
        question.setUpdatedAt(LocalDateTime.now());
        questionMapper.updateById(question);
        return Result.success();
    }

    @Operation(summary = "删除题目")
    @DeleteMapping("/questions/{id}")
    public Result<?> deleteQuestion(@PathVariable Long id) {
        questionMapper.deleteById(id);
        return Result.success();
    }

    @Operation(summary = "Excel导入题目")
    @PostMapping("/questions/import")
    public Result<?> importQuestions(@RequestParam("file") MultipartFile file) {
        return Result.success(Map.of("message", "导入功能开发中"));
    }

    // ==================== User Management ====================

    @Operation(summary = "用户列表")
    @GetMapping("/users")
    public Result<?> users(@RequestParam(defaultValue = "1") int page,
                           @RequestParam(defaultValue = "15") int size,
                           @RequestParam(required = false) String keyword,
                           @RequestParam(required = false) Integer status) {
        LambdaQueryWrapper<User> w = new LambdaQueryWrapper<>();
        if (keyword != null && !keyword.isEmpty()) {
            w.and(wr -> wr.like(User::getUsername, keyword).or().like(User::getNickname, keyword).or().like(User::getEmail, keyword));
        }
        if (status != null) w.eq(User::getStatus, status);
        w.orderByDesc(User::getCreatedAt);
        Page<User> p = new Page<>(page, size);
        userMapper.selectPage(p, w);
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("records", p.getRecords().stream().map(u -> {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("id", u.getId());
            m.put("username", u.getUsername());
            m.put("nickname", u.getNickname());
            m.put("email", u.getEmail());
            m.put("role", u.getRole());
            m.put("status", u.getStatus());
            m.put("createdAt", u.getCreatedAt());
            Long done = userAnswerMapper.countByUser(u.getId());
            m.put("totalDone", done != null ? done : 0);
            m.put("lastActive", getUserLastActive(u.getId()));
            return m;
        }).collect(Collectors.toList()));
        result.put("total", p.getTotal());
        result.put("page", page);
        result.put("size", size);
        return Result.success(result);
    }

    @Operation(summary = "用户详情")
    @GetMapping("/users/{id}")
    public Result<?> userDetail(@PathVariable Long id) {
        User u = userMapper.selectById(id);
        if (u == null) throw new BusinessException(404, "用户不存在");
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("id", u.getId());
        result.put("username", u.getUsername());
        result.put("nickname", u.getNickname());
        result.put("email", u.getEmail());
        result.put("role", u.getRole());
        result.put("status", u.getStatus());
        result.put("createdAt", u.getCreatedAt());
        result.put("totalDone", userAnswerMapper.countByUser(id));
        result.put("correctCount", userAnswerMapper.countCorrectByUser(id));
        result.put("studyDays", userAnswerMapper.countStudyDays(id));
        // Recent answers
        List<Map<String, Object>> recent = userAnswerMapper.selectRecentByUser(id, 20);
        result.put("recentAnswers", recent);
        // Daily activity
        result.put("dailyActivity", userAnswerMapper.dailyCount(id, LocalDate.now().minusDays(30)));
        // Subject distribution
        result.put("subjectStats", userAnswerMapper.subjectStats(id));
        return Result.success(result);
    }

    @Operation(summary = "更新用户状态")
    @PutMapping("/users/{id}/status")
    public Result<?> updateUserStatus(@PathVariable Long id, @RequestBody Map<String, Integer> body) {
        User u = userMapper.selectById(id);
        if (u == null) throw new BusinessException(404, "用户不存在");
        u.setStatus(body.get("status"));
        userMapper.updateById(u);
        return Result.success();
    }

    @Operation(summary = "修改用户角色")
    @PutMapping("/users/{id}/role")
    public Result<?> updateUserRole(@PathVariable Long id, @RequestBody Map<String, String> body) {
        User u = userMapper.selectById(id);
        if (u == null) throw new BusinessException(404, "用户不存在");
        u.setRole(body.get("role"));
        userMapper.updateById(u);
        return Result.success();
    }

    // ==================== Platform Analytics ====================

    @Operation(summary = "平台总览统计")
    @GetMapping("/analytics/overview")
    public Result<?> analyticsOverview() {
        Map<String, Object> result = new LinkedHashMap<>();
        Long totalUsers = userMapper.selectCount(null);
        Long totalQuestions = questionMapper.selectCount(null);
        result.put("totalUsers", totalUsers);
        result.put("totalQuestions", totalQuestions);
        result.put("totalSubjects", subjectMapper.selectCount(null));
        // total answers
        Long totalAnswers = userAnswerMapper.selectCount(null);
        result.put("totalAnswers", totalAnswers != null ? totalAnswers : 0);
        // today
        result.put("todayAnswers", userAnswerMapper.countTodayTotal());
        result.put("todayActiveUsers", userAnswerMapper.countTodayActiveUsers());
        return Result.success(result);
    }

    @Operation(summary = "在线用户列表")
    @GetMapping("/analytics/online")
    public Result<?> onlineUsers() {
        long fiveMinAgo = System.currentTimeMillis() - 5 * 60 * 1000;
        List<Map<String, Object>> online = userAnswerMapper.getOnlineUsers(
                new java.sql.Timestamp(fiveMinAgo).toLocalDateTime());
        return Result.success(online);
    }

    @Operation(summary = "每日活跃用户趋势(近30天)")
    @GetMapping("/analytics/daily-active")
    public Result<?> dailyActiveUsers() {
        return Result.success(userAnswerMapper.dailyActiveUsers(30));
    }

    @Operation(summary = "近30天刷题量趋势")
    @GetMapping("/analytics/daily-practice")
    public Result<?> dailyPractice() {
        List<Map<String, Object>> data = userAnswerMapper.dailyPracticeCount(30);
        return Result.success(data);
    }

    @Operation(summary = "实时在线人数趋势(近24h)")
    @GetMapping("/analytics/online-trend")
    public Result<?> onlineTrend() {
        List<Map<String, Object>> data = new ArrayList<>();
        LocalDateTime now = LocalDateTime.now();
        for (int i = 23; i >= 0; i--) {
            LocalDateTime start = now.minusHours(i + 1);
            LocalDateTime end = now.minusHours(i);
            Long count = userAnswerMapper.countActiveBetween(start, end);
            Map<String, Object> point = new LinkedHashMap<>();
            point.put("hour", String.format("%02d:00", (now.getHour() - i + 24) % 24));
            point.put("count", count != null ? count : 0);
            data.add(point);
        }
        return Result.success(data);
    }

    @Operation(summary = "每日卷王(今日刷题TOP10)")
    @GetMapping("/analytics/daily-top")
    public Result<?> dailyTop() {
        return Result.success(userAnswerMapper.dailyTopUsers(10));
    }

    @Operation(summary = "刷题总榜(总刷题TOP20)")
    @GetMapping("/analytics/total-top")
    public Result<?> totalTop() {
        return Result.success(userAnswerMapper.totalTopUsers(20));
    }

    @Operation(summary = "科目刷题分布")
    @GetMapping("/analytics/subject-distribution")
    public Result<?> subjectDistribution() {
        return Result.success(userAnswerMapper.subjectDistribution());
    }

    // ==================== Invite Code Management ====================

    @Operation(summary = "邀请码列表")
    @GetMapping("/invite-codes")
    public Result<?> inviteCodeList(@RequestParam(defaultValue = "1") int page,
                                    @RequestParam(defaultValue = "20") int size) {
        int offset = (page - 1) * size;
        List<Map<String, Object>> list = inviteCodeMapper.pageQuery(size, offset);
        long total = inviteCodeMapper.countAll();
        long unused = inviteCodeMapper.countUnused();
        Map<String, Object> result = new HashMap<>();
        result.put("list", list);
        result.put("total", total);
        result.put("unused", unused);
        result.put("page", page);
        result.put("size", size);
        return Result.success(result);
    }

    @Operation(summary = "批量生成邀请码")
    @PostMapping("/invite-codes/generate")
    public Result<?> generateInviteCodes(@RequestBody Map<String, Integer> body) {
        int count = body.getOrDefault("count", 10);
        if (count < 1 || count > 100) throw new BusinessException("生成数量需在1-100之间");
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        List<String> codes = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            String code = UUID.randomUUID().toString().replace("-", "").substring(0, 12).toUpperCase();
            InviteCode ic = new InviteCode();
            ic.setCode(code);
            ic.setUsed(0);
            ic.setCreatedBy(userId);
            inviteCodeMapper.insert(ic);
            codes.add(code);
        }
        Map<String, Object> result = new HashMap<>();
        result.put("generated", codes.size());
        result.put("codes", codes);
        return Result.success(result);
    }

    @Operation(summary = "删除邀请码")
    @DeleteMapping("/invite-codes/{id}")
    public Result<?> deleteInviteCode(@PathVariable Long id) {
        inviteCodeMapper.deleteById(id);
        return Result.success();
    }

    // ==================== Helpers ====================

    private String getUserLastActive(Long userId) {
        try {
            Map<String, Object> last = userAnswerMapper.selectLastActive(userId);
            if (last != null && last.get("answered_at") != null) {
                return last.get("answered_at").toString();
            }
        } catch (Exception ignored) {}
        return null;
    }
}
