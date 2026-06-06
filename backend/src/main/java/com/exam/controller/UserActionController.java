package com.exam.controller;

import com.exam.common.Result;
import com.exam.entity.UserQuestionMastery;
import com.exam.mapper.UserQuestionMasteryMapper;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.FavoriteService;
import com.exam.service.NoteService;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Tag(name = "收藏与笔记接口")
@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
public class UserActionController {

    private final FavoriteService favoriteService;
    private final NoteService noteService;
    private final UserQuestionMasteryMapper masteryMapper;

    @Operation(summary = "切换收藏状态")
    @PostMapping("/favorite/{questionId}")
    public Result<?> toggleFavorite(@PathVariable Long questionId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        favoriteService.toggle(userId, questionId);
        return Result.success(Map.of("isFavorited", favoriteService.isFavorited(userId, questionId)));
    }

    @Operation(summary = "收藏列表")
    @GetMapping("/favorites")
    public Result<?> favorites() {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(favoriteService.listByUser(userId));
    }

    @Operation(summary = "保存笔记")
    @PostMapping("/note/{questionId}")
    public Result<?> saveNote(@PathVariable Long questionId, @RequestBody Map<String, String> body) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(noteService.saveOrUpdate(userId, questionId, body.get("content")));
    }

    @Operation(summary = "获取题目笔记")
    @GetMapping("/note/{questionId}")
    public Result<?> getNote(@PathVariable Long questionId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(noteService.getByQuestion(userId, questionId));
    }

    @Operation(summary = "笔记列表")
    @GetMapping("/notes")
    public Result<?> notes() {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(noteService.listByUser(userId));
    }

    @Operation(summary = "删除笔记")
    @DeleteMapping("/note/{noteId}")
    public Result<?> deleteNote(@PathVariable Long noteId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        noteService.delete(userId, noteId);
        return Result.success();
    }

    @Operation(summary = "设置掌握程度")
    @PostMapping("/mastery/{questionId}")
    public Result<?> setMastery(@PathVariable Long questionId, @RequestBody Map<String, String> body) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        String level = body.get("mastery");
        UserQuestionMastery existing = masteryMapper.selectOne(
            new LambdaQueryWrapper<UserQuestionMastery>()
                .eq(UserQuestionMastery::getUserId, userId)
                .eq(UserQuestionMastery::getQuestionId, questionId));
        if (existing != null) {
            existing.setMastery(level);
            masteryMapper.updateById(existing);
        } else {
            UserQuestionMastery m = new UserQuestionMastery();
            m.setUserId(userId);
            m.setQuestionId(questionId);
            m.setMastery(level);
            masteryMapper.insert(m);
        }
        return Result.success(Map.of("questionId", questionId, "mastery", level));
    }

    @Operation(summary = "获取所有掌握程度")
    @GetMapping("/mastery")
    public Result<?> getMastery() {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        List<Map<String, Object>> list = masteryMapper.selectByUserId(userId);
        Map<Long, String> result = new HashMap<>();
        for (Map<String, Object> m : list) {
            result.put(((Number) m.get("question_id")).longValue(), (String) m.get("mastery"));
        }
        return Result.success(result);
    }
}