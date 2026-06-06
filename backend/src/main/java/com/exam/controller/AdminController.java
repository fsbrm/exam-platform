package com.exam.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.exam.common.BusinessException;
import com.exam.common.Result;
import com.exam.dto.QuestionQueryDTO;
import com.exam.entity.InviteCode;
import com.exam.entity.Question;
import com.exam.mapper.InviteCodeMapper;
import com.exam.mapper.QuestionMapper;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.DashboardService;
import com.exam.service.QuestionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.*;

@Tag(name = "管理后台接口")
@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {

    private final QuestionService questionService;
    private final QuestionMapper questionMapper;
    private final DashboardService dashboardService;
    private final InviteCodeMapper inviteCodeMapper;

    @Operation(summary = "题目列表")
    @GetMapping("/questions")
    public Result<?> questions(QuestionQueryDTO dto) {
        return Result.success(questionService.pageQuery(dto));
    }

    @Operation(summary = "新增题目")
    @PostMapping("/questions")
    public Result<?> addQuestion(@RequestBody Question question) {
        questionMapper.insert(question);
        return Result.success(question);
    }

    @Operation(summary = "更新题目")
    @PutMapping("/questions/{id}")
    public Result<?> updateQuestion(@PathVariable Long id, @RequestBody Question question) {
        question.setId(id);
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
        return Result.success(Map.of("message", "导入功能开发中，请使用题目管理界面手动添加"));
    }

    @Operation(summary = "数据看板")
    @GetMapping("/stats")
    public Result<?> stats() {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId != null) {
            return Result.success(dashboardService.getUserDashboard(userId));
        }
        return Result.error("未登录");
    }

    // ========== Invite Code Management ==========

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
        if (count < 1 || count > 100) {
            throw new BusinessException("生成数量需在1-100之间");
        }
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
}