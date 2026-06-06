package com.exam.vo;

import lombok.Builder;
import lombok.Data;
import java.math.BigDecimal;

@Data
@Builder
public class ExamResultVO {
    private Long examId;
    private Integer totalQuestions;
    private Integer correctCount;
    private BigDecimal score;
    private Integer duration;
    private Integer timeLimit;
    private String status;
}
