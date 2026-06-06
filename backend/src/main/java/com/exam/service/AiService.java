package com.exam.service;

import java.util.Map;

public interface AiService {
    Map<String, Object> chat(Long userId, String question, String context);
    Map<String, Object> analyzeWeakPoints(Long userId, Long subjectId);
}
