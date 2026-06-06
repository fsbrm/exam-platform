package com.exam.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("chapter")
public class Chapter {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long subjectId;
    private String name;
    private String description;
    private Long parentId;
    private Integer sortOrder;
    private Integer questionCount;
    private LocalDateTime createdAt;
}
