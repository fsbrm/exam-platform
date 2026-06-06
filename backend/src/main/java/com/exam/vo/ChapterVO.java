package com.exam.vo;

import lombok.Data;

@Data
public class ChapterVO {
    private Long id;
    private String name;
    private String description;
    private Integer questionCount;
    private Long parentId;
    private Integer sortOrder;
}
