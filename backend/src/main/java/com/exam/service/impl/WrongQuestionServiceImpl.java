package com.exam.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.common.BusinessException;
import com.exam.entity.Question;
import com.exam.entity.WrongQuestion;
import com.exam.mapper.QuestionMapper;
import com.exam.mapper.WrongQuestionMapper;
import com.exam.service.WrongQuestionService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class WrongQuestionServiceImpl implements WrongQuestionService {

    private final WrongQuestionMapper wrongQuestionMapper;
    private final QuestionMapper questionMapper;

    @Override
    public List<WrongQuestion> listByUser(Long userId, Long subjectId) {
        LambdaQueryWrapper<WrongQuestion> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(WrongQuestion::getUserId, userId)
               .eq(WrongQuestion::getIsRemoved, 0);
        if (subjectId != null) wrapper.eq(WrongQuestion::getSubjectId, subjectId);
        wrapper.orderByDesc(WrongQuestion::getLastWrongAt);
        return wrongQuestionMapper.selectList(wrapper);
    }

    @Override
    public Map<String, Object> getPracticeList(Long userId, Long subjectId) {
        List<WrongQuestion> wrongs = listByUser(userId, subjectId);
        List<Long> questionIds = wrongs.stream()
                .map(WrongQuestion::getQuestionId).collect(Collectors.toList());

        List<Question> questions = Collections.emptyList();
        if (!questionIds.isEmpty()) {
            questions = questionMapper.selectBatchIds(questionIds);
        }

        Map<String, Object> result = new HashMap<>();
        result.put("total", questions.size());
        result.put("questions", questions);
        return result;
    }

    @Override
    public void removeWrong(Long userId, Long questionId) {
        WrongQuestion wq = wrongQuestionMapper.selectOne(
                new LambdaQueryWrapper<WrongQuestion>()
                        .eq(WrongQuestion::getUserId, userId)
                        .eq(WrongQuestion::getQuestionId, questionId)
        );
        if (wq == null) throw new BusinessException("错题记录不存在");
        wq.setIsRemoved(1);
        wrongQuestionMapper.updateById(wq);
    }
}
