package com.exam.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("user_answer")
public class UserAnswer {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long userId;
    private Long questionId;
    private Long subjectId;
    private String userAnswer;
    private Integer isCorrect;
    private LocalDateTime answeredAt;
}
