package com.exam.service;

import com.exam.entity.Chapter;
import com.exam.entity.Subject;
import java.util.List;

public interface SubjectService {
    List<Subject> listAll();
    List<Chapter> getChapters(Long subjectId);
}
