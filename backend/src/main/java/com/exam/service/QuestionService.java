package com.exam.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.exam.dto.QuestionQueryDTO;
import com.exam.entity.Question;
import com.exam.vo.QuestionVO;
import java.util.List;

public interface QuestionService {
    Page<Question> pageQuery(QuestionQueryDTO dto);
    QuestionVO getDetail(Long questionId, Long userId);
    List<Question> getPracticeQuestions(Long subjectId, Long chapterId, Long knowledgeId, int count);
    List<Question> getRandomQuestions(Long subjectId, int count);
}
