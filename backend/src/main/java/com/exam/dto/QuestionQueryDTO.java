package com.exam.dto;

import lombok.Data;

@Data
public class QuestionQueryDTO {
    private Long subjectId;
    private Long chapterId;
    private String type;
    private String difficulty;
    private Integer year;
    private String keyword;
    private Integer pageNum = 1;
    private Integer pageSize = 10;
}
