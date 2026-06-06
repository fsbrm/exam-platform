package com.exam.controller;

import com.exam.common.Result;
import com.exam.dto.AiChatDTO;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.AiService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@Tag(name = "AI助手接口")
@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiService aiService;

    @Operation(summary = "AI对话")
    @PostMapping("/chat")
    public Result<?> chat(@RequestBody AiChatDTO dto) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(aiService.chat(userId, dto.getQuestion(), dto.getContext()));
    }

    @Operation(summary = "AI薄弱点分析")
    @GetMapping("/analyze/{subjectId}")
    public Result<?> analyze(@PathVariable Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(aiService.analyzeWeakPoints(userId, subjectId));
    }
}
