package com.exam.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("exam_record")
public class ExamRecord {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long userId;
    private Long subjectId;
    private Integer totalQuestions;
    private Integer correctCount;
    private BigDecimal score;
    private Integer duration;
    private Integer timeLimit;
    private String status;
    private LocalDateTime startedAt;
    private LocalDateTime finishedAt;
}
