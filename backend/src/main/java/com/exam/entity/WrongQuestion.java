package com.exam.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("wrong_question")
public class WrongQuestion {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long userId;
    private Long questionId;
    private Long subjectId;
    private Integer wrongCount;
    private LocalDateTime lastWrongAt;
    private Integer isRemoved;
}
