package com.exam.service;

import com.exam.dto.ExamStartDTO;
import com.exam.vo.ExamResultVO;
import java.util.List;
import java.util.Map;

public interface PracticeService {
    Map<String, Object> submitAnswer(Long userId, Long questionId, String answer);
    Map<String, Object> startExam(Long userId, ExamStartDTO dto);
    ExamResultVO finishExam(Long userId, Long examId);
    ExamResultVO timeoutExam(Long userId, Long examId);
    Map<String, Object> getExamDetail(Long userId, Long examId);
    List<Map<String, Object>> getExamHistory(Long userId, Long subjectId);
}
