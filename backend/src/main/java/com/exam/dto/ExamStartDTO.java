package com.exam.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class ExamStartDTO {
    @NotNull(message = "科目不能为空")
    private Long subjectId;

    @NotNull(message = "题目数量不能为空")
    private Integer questionCount;

    @NotNull(message = "考试时长不能为空")
    private Integer timeLimit;
}
