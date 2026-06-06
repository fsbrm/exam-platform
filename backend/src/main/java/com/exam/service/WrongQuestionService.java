package com.exam.service;

import com.exam.entity.WrongQuestion;
import java.util.List;
import java.util.Map;

public interface WrongQuestionService {
    List<WrongQuestion> listByUser(Long userId, Long subjectId);
    Map<String, Object> getPracticeList(Long userId, Long subjectId);
    void removeWrong(Long userId, Long questionId);
}
