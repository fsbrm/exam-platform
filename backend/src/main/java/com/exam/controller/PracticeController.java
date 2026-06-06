package com.exam.controller;

import com.exam.common.Result;
import com.exam.dto.ExamStartDTO;
import com.exam.dto.SubmitAnswerDTO;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.PracticeService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@Tag(name = "刷题与考试接口")
@RestController
@RequestMapping("/api/practice")
@RequiredArgsConstructor
public class PracticeController {

    private final PracticeService practiceService;

    @Operation(summary = "提交答案")
    @PostMapping("/submit")
    public Result<?> submitAnswer(@Valid @RequestBody SubmitAnswerDTO dto) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(practiceService.submitAnswer(userId, dto.getQuestionId(), dto.getAnswer()));
    }

    @Operation(summary = "开始考试")
    @PostMapping("/exam/start")
    public Result<?> startExam(@Valid @RequestBody ExamStartDTO dto) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(practiceService.startExam(userId, dto));
    }

    @Operation(summary = "提交考试")
    @PostMapping("/exam/{examId}/submit")
    public Result<?> submitExam(@PathVariable Long examId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(practiceService.finishExam(userId, examId));
    }

    @Operation(summary = "考试超时")
    @PostMapping("/exam/{examId}/timeout")
    public Result<?> timeoutExam(@PathVariable Long examId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(practiceService.timeoutExam(userId, examId));
    }

    @Operation(summary = "考试详情回顾")
    @GetMapping("/exam/{examId}")
    public Result<?> examDetail(@PathVariable Long examId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(practiceService.getExamDetail(userId, examId));
    }

    @Operation(summary = "考试历史")
    @GetMapping("/exam/history")
    public Result<?> examHistory(@RequestParam(required = false) Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(practiceService.getExamHistory(userId, subjectId));
    }

    @Operation(summary = "考试中提交单题答案")
    @PostMapping("/exam/{examId}/answer")
    public Result<?> examAnswer(@PathVariable Long examId, @Valid @RequestBody SubmitAnswerDTO dto) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(practiceService.submitAnswer(userId, dto.getQuestionId(), dto.getAnswer()));
    }
}
