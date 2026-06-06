package com.exam.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("question")
public class Question {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long chapterId;
    private Long subjectId;
    private String type;
    private String difficulty;
    private String content;
    private String options;
    private String answer;
    private String image;
    private String videoUrl;
    private String analysis;
    private Integer year;
    private Integer status;
    @TableField(exist = false)
    private Integer questionNumber;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
