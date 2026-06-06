package com.exam.controller;

import com.exam.common.Result;
import com.exam.mapper.WrongQuestionMapper;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.WrongQuestionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@Tag(name = "错题本接口")
@RestController
@RequestMapping("/api/wrong")
@RequiredArgsConstructor
public class WrongQuestionController {

    private final WrongQuestionService wrongQuestionService;
    private final WrongQuestionMapper wrongQuestionMapper;

    @Operation(summary = "错题列表")
    @GetMapping
    public Result<?> list(@RequestParam(required = false) Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(wrongQuestionService.listByUser(userId, subjectId));
    }

    @Operation(summary = "增强错题列表(含错因/收藏/筛选)")
    @GetMapping("/enhanced")
    public Result<?> enhanced(
            @RequestParam(required = false) Long subjectId,
            @RequestParam(required = false) Long chapterId,
            @RequestParam(required = false) String mastery,
            @RequestParam(required = false) Boolean favoriteOnly,
            @RequestParam(required = false) String yearMonth) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        List<Map<String, Object>> all = wrongQuestionMapper.selectEnhancedAll(userId);
        // Filter in Java
        List<Map<String, Object>> filtered = new ArrayList<>();
        for (Map<String, Object> q : all) {
            if (subjectId != null && !subjectId.equals(q.get("subject_id"))) continue;
            if (chapterId != null && !chapterId.equals(q.get("chapter_id"))) continue;
            if (mastery != null && !mastery.isEmpty() && !mastery.equals(q.get("mastery"))) continue;
            if (favoriteOnly != null && favoriteOnly && !Integer.valueOf(1).equals(q.get("is_favorited"))) continue;
            if (yearMonth != null && !yearMonth.isEmpty()) {
                Object lastWrong = q.get("last_wrong_at");
                if (lastWrong == null || !lastWrong.toString().substring(0, 7).equals(yearMonth)) continue;
            }
            filtered.add(q);
        }
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("questions", filtered);
        result.put("total", filtered.size());
        return Result.success(result);
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
