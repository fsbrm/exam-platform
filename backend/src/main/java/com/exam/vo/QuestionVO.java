package com.exam.vo;

import lombok.Data;

@Data
public class QuestionVO {
    private Long id;
    private Long chapterId;
    private Long subjectId;
    private String type;
    private String difficulty;
    private String content;
    private String options;
    private String answer;
    private String image;
    private String analysis;
    private Boolean isFavorited;
    private Boolean hasNote;
    private Integer year;
    private Integer questionNumber;
}