package com.exam.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.exam.dto.QuestionQueryDTO;
import com.exam.entity.Favorite;
import com.exam.entity.Note;
import com.exam.entity.Question;
import com.exam.mapper.FavoriteMapper;
import com.exam.mapper.NoteMapper;
import com.exam.mapper.QuestionMapper;
import com.exam.service.QuestionService;
import com.exam.vo.QuestionVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class QuestionServiceImpl implements QuestionService {

    private final QuestionMapper questionMapper;
    private final FavoriteMapper favoriteMapper;
    private final NoteMapper noteMapper;

    @Override
    public Page<Question> pageQuery(QuestionQueryDTO dto) {
        LambdaQueryWrapper<Question> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Question::getStatus, 1);
        if (dto.getSubjectId() != null) wrapper.eq(Question::getSubjectId, dto.getSubjectId());
        if (dto.getChapterId() != null) wrapper.eq(Question::getChapterId, dto.getChapterId());
        if (dto.getYear() != null) wrapper.eq(Question::getYear, dto.getYear());
        if (dto.getType() != null) wrapper.eq(Question::getType, dto.getType());
        if (dto.getDifficulty() != null) wrapper.eq(Question::getDifficulty, dto.getDifficulty());
        if (dto.getKeyword() != null) wrapper.like(Question::getContent, dto.getKeyword());
        wrapper.orderByDesc(Question::getId);

        return questionMapper.selectPage(
                new Page<>(dto.getPageNum(), dto.getPageSize()), wrapper);
    }

    @Override
    @Transactional
    public QuestionVO getDetail(Long questionId, Long userId) {
        Question q = questionMapper.selectById(questionId);
        if (q == null) return null;

        QuestionVO vo = new QuestionVO();
        vo.setId(q.getId());
        vo.setChapterId(q.getChapterId());
        vo.setSubjectId(q.getSubjectId());
        vo.setType(q.getType());
        vo.setDifficulty(q.getDifficulty());
        vo.setContent(q.getContent());
        vo.setOptions(q.getOptions());
        vo.setAnswer(q.getAnswer());
        vo.setImage(q.getImage());
        vo.setAnalysis(q.getAnalysis());
        vo.setYear(q.getYear());
        vo.setQuestionNumber(questionMapper.selectQuestionNumber(questionId));

        if (userId != null) {
            Long favCount = favoriteMapper.selectCount(
                    new LambdaQueryWrapper<Favorite>()
                            .eq(Favorite::getUserId, userId)
                            .eq(Favorite::getQuestionId, questionId)
            );
            vo.setIsFavorited(favCount > 0);

            Long noteCount = noteMapper.selectCount(
                    new LambdaQueryWrapper<Note>()
                            .eq(Note::getUserId, userId)
                            .eq(Note::getQuestionId, questionId)
            );
            vo.setHasNote(noteCount > 0);
        }

        return vo;
    }

    @Override
    public List<Question> getPracticeQuestions(Long subjectId, Long chapterId, Long knowledgeId, int count) {
        if (knowledgeId != null) {
            return questionMapper.selectByKnowledgeId(knowledgeId);
        }
        if (chapterId != null) {
            return questionMapper.selectByChapter(chapterId);
        }
        if (subjectId != null) {
            return questionMapper.selectBySubject(subjectId);
        }
        return questionMapper.selectAll();
    }

    @Override
    public List<Question> getRandomQuestions(Long subjectId, int count) {
        return questionMapper.selectBySubject(subjectId);
    }
}
