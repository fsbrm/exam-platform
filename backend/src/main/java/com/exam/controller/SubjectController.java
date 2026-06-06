package com.exam.controller;

import com.exam.common.Result;
import com.exam.service.SubjectService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@Tag(name = "科目章节接口")
@RestController
@RequestMapping("/api/subjects")
@RequiredArgsConstructor
public class SubjectController {

    private final SubjectService subjectService;

    @Operation(summary = "获取所有科目")
    @GetMapping
    public Result<?> listAll() {
        return Result.success(subjectService.listAll());
    }

    @Operation(summary = "获取科目章节")
    @GetMapping("/{subjectId}/chapters")
    public Result<?> getChapters(@PathVariable Long subjectId) {
        return Result.success(subjectService.getChapters(subjectId));
    }
}
