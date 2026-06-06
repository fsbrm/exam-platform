package com.exam.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.entity.Chapter;
import com.exam.entity.Subject;
import com.exam.mapper.ChapterMapper;
import com.exam.mapper.SubjectMapper;
import com.exam.service.SubjectService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class SubjectServiceImpl implements SubjectService {

    private final SubjectMapper subjectMapper;
    private final ChapterMapper chapterMapper;

    @Override
    public List<Subject> listAll() {
        return subjectMapper.selectList(
                new LambdaQueryWrapper<Subject>()
                        .eq(Subject::getStatus, 1)
                        .orderByAsc(Subject::getSortOrder)
        );
    }

    @Override
    public List<Chapter> getChapters(Long subjectId) {
        return chapterMapper.selectList(
                new LambdaQueryWrapper<Chapter>()
                        .eq(Chapter::getSubjectId, subjectId)
                        .orderByAsc(Chapter::getSortOrder)
        );
    }
}
