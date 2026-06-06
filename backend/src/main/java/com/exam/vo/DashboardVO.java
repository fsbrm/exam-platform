package com.exam.vo;

import lombok.Builder;
import lombok.Data;
import java.math.BigDecimal;

@Data
@Builder
public class DashboardVO {
    private Long totalQuestions;
    private Long correctQuestions;
    private BigDecimal accuracy;
    private Integer studyDays;
    private Integer streakDays;
}
