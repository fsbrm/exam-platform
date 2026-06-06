package com.exam.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("invite_code")
public class InviteCode {
    @TableId(type = IdType.AUTO)
    private Long id;
    private String code;
    private Integer used;
    private Long usedBy;
    private LocalDateTime usedAt;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    private Long createdBy;
}