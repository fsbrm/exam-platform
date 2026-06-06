package com.exam.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("user_question_mastery")
public class UserQuestionMastery {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long userId;
    private Long questionId;
    private String mastery;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}