package com.exam.service;

import com.exam.entity.Note;
import java.util.List;

public interface NoteService {
    Note saveOrUpdate(Long userId, Long questionId, String content);
    Note getByQuestion(Long userId, Long questionId);
    List<Note> listByUser(Long userId);
    void delete(Long userId, Long noteId);
}
