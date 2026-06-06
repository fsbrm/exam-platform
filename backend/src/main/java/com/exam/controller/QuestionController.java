package com.exam.controller;

import com.exam.common.Result;
import com.exam.dto.QuestionQueryDTO;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.QuestionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@Tag(name = "题库接口")
@RestController
@RequestMapping("/api/questions")
@RequiredArgsConstructor
public class QuestionController {

    private final QuestionService questionService;

    @Operation(summary = "分页查询题目")
    @GetMapping
    public Result<?> list(QuestionQueryDTO dto) {
        return Result.success(questionService.pageQuery(dto));
    }

    @Operation(summary = "查看题目详情")
    @GetMapping("/{id}")
    public Result<?> detail(@PathVariable Long id) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        return Result.success(questionService.getDetail(id, userId));
    }

    @Operation(summary = "章节练习-获取题目列表")
    @GetMapping("/practice")
    public Result<?> practice(@RequestParam(required = false) Long subjectId, @RequestParam(required = false) Long chapterId, @RequestParam(required = false) Long knowledgeId, @RequestParam(defaultValue = "20") int count) { return Result.success(questionService.getPracticeQuestions(subjectId, chapterId, knowledgeId, count));
    }

    @Operation(summary = "随机练习-获取题目列表")
    @GetMapping("/random")
    public Result<?> random(@RequestParam Long subjectId, @RequestParam(defaultValue = "10") int count) {
        return Result.success(questionService.getRandomQuestions(subjectId, count));
    }
}
