package com.exam.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("exam_paper")
public class ExamPaper {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long subjectId;
    private Integer year;
    private String name;
    private Integer totalScore;
    private Integer duration;
    private Integer questionCount;
    private Integer sortOrder;
    private LocalDateTime createdAt;
}