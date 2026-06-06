package com.exam.controller;

import com.exam.common.Result;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.WrongQuestionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@Tag(name = "错题本接口")
@RestController
@RequestMapping("/api/wrong")
@RequiredArgsConstructor
public class WrongQuestionController {

    private final WrongQuestionService wrongQuestionService;

    @Operation(summary = "错题列表")
    @GetMapping
    public Result<?> list(@RequestParam(required = false) Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(wrongQuestionService.listByUser(userId, subjectId));
    }

    @Operation(summary = "错题重做-获取题目")
    @GetMapping("/practice")
    public Result<?> practice(@RequestParam(required = false) Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        Map<String, Object> data = wrongQuestionService.getPracticeList(userId, subjectId);
        return Result.success(data);
    }

    @Operation(summary = "移除错题")
    @DeleteMapping("/{questionId}")
    public Result<?> remove(@PathVariable Long questionId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        wrongQuestionService.removeWrong(userId, questionId);
        return Result.success();
    }
}
