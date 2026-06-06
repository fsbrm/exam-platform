package com.exam.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.common.BusinessException;
import com.exam.dto.ExamStartDTO;
import com.exam.entity.*;
import com.exam.mapper.*;
import com.exam.service.PracticeService;
import com.exam.vo.ExamResultVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class PracticeServiceImpl implements PracticeService {

    private final UserAnswerMapper userAnswerMapper;
    private final QuestionMapper questionMapper;
    private final ExamRecordMapper examRecordMapper;
    private final ExamQuestionMapper examQuestionMapper;
    private final WrongQuestionMapper wrongQuestionMapper;

    @Override
    @Transactional
    public Map<String, Object> submitAnswer(Long userId, Long questionId, String answer) {
        Question question = questionMapper.selectById(questionId);
        if (question == null) {
            throw new BusinessException("题目不存在");
        }

        boolean isCorrect = question.getAnswer().equals(answer);

        // 保存答题记录
        UserAnswer ua = new UserAnswer();
        ua.setUserId(userId);
        ua.setQuestionId(questionId);
        ua.setSubjectId(question.getSubjectId());
        ua.setUserAnswer(answer);
        ua.setIsCorrect(isCorrect ? 1 : 0);
        ua.setAnsweredAt(LocalDateTime.now());
        userAnswerMapper.insert(ua);

        // 错题处理
        if (!isCorrect) {
            WrongQuestion wq = wrongQuestionMapper.selectOne(
                    new LambdaQueryWrapper<WrongQuestion>()
                            .eq(WrongQuestion::getUserId, userId)
                            .eq(WrongQuestion::getQuestionId, questionId)
            );
            if (wq == null) {
                wq = new WrongQuestion();
                wq.setUserId(userId);
                wq.setQuestionId(questionId);
                wq.setSubjectId(question.getSubjectId());
                wq.setWrongCount(1);
                wq.setLastWrongAt(LocalDateTime.now());
                wrongQuestionMapper.insert(wq);
            } else {
                wq.setWrongCount(wq.getWrongCount() + 1);
                wq.setLastWrongAt(LocalDateTime.now());
                wq.setIsRemoved(0);
                wrongQuestionMapper.updateById(wq);
            }
        }

        Map<String, Object> result = new HashMap<>();
        result.put("isCorrect", isCorrect);
        result.put("answer", question.getAnswer());
        result.put("analysis", question.getAnalysis());
        return result;
    }

    @Override
    @Transactional
    public Map<String, Object> startExam(Long userId, ExamStartDTO dto) {
        // 随机抽题
        List<Question> questions = questionMapper.selectRandomBySubject(dto.getSubjectId(), dto.getQuestionCount());
        if (questions.isEmpty()) {
            throw new BusinessException("该科目暂无题目");
        }

        // 创建考试记录
        ExamRecord exam = new ExamRecord();
        exam.setUserId(userId);
        exam.setSubjectId(dto.getSubjectId());
        exam.setTotalQuestions(questions.size());
        exam.setTimeLimit(dto.getTimeLimit());
        exam.setStatus("IN_PROGRESS");
        exam.setStartedAt(LocalDateTime.now());
        examRecordMapper.insert(exam);

        // 关联题目
        List<Map<String, Object>> questionList = new ArrayList<>();
        for (int i = 0; i < questions.size(); i++) {
            Question q = questions.get(i);
            ExamQuestion eq = new ExamQuestion();
            eq.setExamId(exam.getId());
            eq.setQuestionId(q.getId());
            eq.setSortOrder(i + 1);
            examQuestionMapper.insert(eq);

            Map<String, Object> qm = new HashMap<>();
            qm.put("id", q.getId());
            qm.put("type", q.getType());
            qm.put("difficulty", q.getDifficulty());
            qm.put("content", q.getContent());
            qm.put("options", q.getOptions());
            qm.put("sortOrder", i + 1);
            questionList.add(qm);
        }

        Map<String, Object> result = new HashMap<>();
        result.put("examId", exam.getId());
        result.put("totalQuestions", questions.size());
        result.put("timeLimit", dto.getTimeLimit());
        result.put("questions", questionList);
        return result;
    }

    @Override
    @Transactional
    public ExamResultVO finishExam(Long userId, Long examId) {
        ExamRecord exam = examRecordMapper.selectById(examId);
        if (exam == null || !exam.getUserId().equals(userId)) {
            throw new BusinessException("考试记录不存在");
        }
        if ("FINISHED".equals(exam.getStatus())) {
            throw new BusinessException("考试已完成");
        }

        // 统计分数
        List<ExamQuestion> eqs = examQuestionMapper.selectList(
                new LambdaQueryWrapper<ExamQuestion>().eq(ExamQuestion::getExamId, examId)
        );
        int correct = (int) eqs.stream().filter(eq -> eq.getIsCorrect() != null && eq.getIsCorrect() == 1).count();

        long duration = ChronoUnit.SECONDS.between(exam.getStartedAt(), LocalDateTime.now());
        BigDecimal score = BigDecimal.valueOf((double) correct / exam.getTotalQuestions() * 100)
                .setScale(1, RoundingMode.HALF_UP);

        exam.setCorrectCount(correct);
        exam.setScore(score);
        exam.setDuration((int) duration);
        exam.setStatus("FINISHED");
        exam.setFinishedAt(LocalDateTime.now());
        examRecordMapper.updateById(exam);

        // 错题处理
        for (ExamQuestion eq : eqs) {
            if (eq.getIsCorrect() != null && eq.getIsCorrect() == 0) {
                Question q = questionMapper.selectById(eq.getQuestionId());
                WrongQuestion wq = wrongQuestionMapper.selectOne(
                        new LambdaQueryWrapper<WrongQuestion>()
                                .eq(WrongQuestion::getUserId, userId)
                                .eq(WrongQuestion::getQuestionId, eq.getQuestionId())
                );
                if (wq == null) {
                    wq = new WrongQuestion();
                    wq.setUserId(userId);
                    wq.setQuestionId(eq.getQuestionId());
                    wq.setSubjectId(q != null ? q.getSubjectId() : exam.getSubjectId());
                    wq.setWrongCount(1);
                    wq.setLastWrongAt(LocalDateTime.now());
                    wrongQuestionMapper.insert(wq);
                } else {
                    wq.setWrongCount(wq.getWrongCount() + 1);
                    wq.setLastWrongAt(LocalDateTime.now());
                    wq.setIsRemoved(0);
                    wrongQuestionMapper.updateById(wq);
                }
            }
        }

        return ExamResultVO.builder()
                .examId(examId)
                .totalQuestions(exam.getTotalQuestions())
                .correctCount(correct)
                .score(score)
                .duration((int) duration)
                .timeLimit(exam.getTimeLimit())
                .status("FINISHED")
                .build();
    }

    @Override
    public ExamResultVO timeoutExam(Long userId, Long examId) {
        ExamRecord exam = examRecordMapper.selectById(examId);
        if (exam != null) {
            exam.setStatus("TIMEOUT");
            exam.setFinishedAt(LocalDateTime.now());
            examRecordMapper.updateById(exam);
        }
        return finishExam(userId, examId);
    }

    @Override
    public Map<String, Object> getExamDetail(Long userId, Long examId) {
        ExamRecord exam = examRecordMapper.selectById(examId);
        if (exam == null) throw new BusinessException("考试记录不存在");

        List<ExamQuestion> eqs = examQuestionMapper.selectList(
                new LambdaQueryWrapper<ExamQuestion>()
                        .eq(ExamQuestion::getExamId, examId)
                        .orderByAsc(ExamQuestion::getSortOrder)
        );

        List<Map<String, Object>> questions = new ArrayList<>();
        for (ExamQuestion eq : eqs) {
            Question q = questionMapper.selectById(eq.getQuestionId());
            Map<String, Object> qm = new HashMap<>();
            qm.put("id", q != null ? q.getId() : null);
            qm.put("content", q != null ? q.getContent() : "");
            qm.put("options", q != null ? q.getOptions() : "");
            qm.put("answer", q != null ? q.getAnswer() : "");
            qm.put("analysis", q != null ? q.getAnalysis() : "");
            qm.put("userAnswer", eq.getUserAnswer());
            qm.put("isCorrect", eq.getIsCorrect());
            qm.put("type", q != null ? q.getType() : "");
            questions.add(qm);
        }

        Map<String, Object> result = new HashMap<>();
        result.put("exam", exam);
        result.put("questions", questions);
        return result;
    }

    @Override
    public List<Map<String, Object>> getExamHistory(Long userId, Long subjectId) {
        LambdaQueryWrapper<ExamRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(ExamRecord::getUserId, userId);
        if (subjectId != null) wrapper.eq(ExamRecord::getSubjectId, subjectId);
        wrapper.orderByDesc(ExamRecord::getStartedAt);

        List<ExamRecord> records = examRecordMapper.selectList(wrapper);
        return records.stream().map(r -> {
            Map<String, Object> m = new HashMap<>();
            m.put("id", r.getId());
            m.put("subjectId", r.getSubjectId());
            m.put("totalQuestions", r.getTotalQuestions());
            m.put("correctCount", r.getCorrectCount());
            m.put("score", r.getScore());
            m.put("duration", r.getDuration());
            m.put("timeLimit", r.getTimeLimit());
            m.put("status", r.getStatus());
            m.put("startedAt", r.getStartedAt());
            return m;
        }).collect(Collectors.toList());
    }
}
