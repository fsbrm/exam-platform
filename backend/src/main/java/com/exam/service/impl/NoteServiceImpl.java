package com.exam.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.common.BusinessException;
import com.exam.entity.Note;
import com.exam.mapper.NoteMapper;
import com.exam.service.NoteService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class NoteServiceImpl implements NoteService {

    private final NoteMapper noteMapper;

    @Override
    @Transactional
    public Note saveOrUpdate(Long userId, Long questionId, String content) {
        Note note = noteMapper.selectOne(
                new LambdaQueryWrapper<Note>()
                        .eq(Note::getUserId, userId)
                        .eq(Note::getQuestionId, questionId)
        );
        if (note == null) {
            note = new Note();
            note.setUserId(userId);
            note.setQuestionId(questionId);
            note.setContent(content);
            note.setCreatedAt(LocalDateTime.now());
            note.setUpdatedAt(LocalDateTime.now());
            noteMapper.insert(note);
        } else {
            note.setContent(content);
            note.setUpdatedAt(LocalDateTime.now());
            noteMapper.updateById(note);
        }
        return note;
    }

    @Override
    public Note getByQuestion(Long userId, Long questionId) {
        return noteMapper.selectOne(
                new LambdaQueryWrapper<Note>()
                        .eq(Note::getUserId, userId)
                        .eq(Note::getQuestionId, questionId)
        );
    }

    @Override
    public List<Note> listByUser(Long userId) {
        return noteMapper.selectList(
                new LambdaQueryWrapper<Note>()
                        .eq(Note::getUserId, userId)
                        .orderByDesc(Note::getUpdatedAt)
        );
    }

    @Override
    public void delete(Long userId, Long noteId) {
        Note note = noteMapper.selectById(noteId);
        if (note == null || !note.getUserId().equals(userId)) {
            throw new BusinessException("笔记不存在");
        }
        noteMapper.deleteById(noteId);
    }
}
