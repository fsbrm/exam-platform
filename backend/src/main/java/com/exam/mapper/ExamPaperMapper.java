package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.ExamPaper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.util.Map;

@Mapper
public interface ExamPaperMapper extends BaseMapper<ExamPaper> {

    @Select("SELECT ep.*, " +
            "COUNT(pq.question_id) AS actual_count " +
            "FROM exam_paper ep " +
            "LEFT JOIN paper_question pq ON ep.id = pq.paper_id " +
            "WHERE ep.subject_id = #{subjectId} " +
            "GROUP BY ep.id ORDER BY ep.year DESC")
    List<Map<String, Object>> selectWithCount(@Param("subjectId") Long subjectId);

    @Select("SELECT q.*, pq.question_number, pq.score " +
            "FROM paper_question pq " +
            "JOIN question q ON pq.question_id = q.id " +
            "WHERE pq.paper_id = #{paperId} " +
            "ORDER BY pq.question_number")
    List<Map<String, Object>> selectQuestionsByPaper(@Param("paperId") Long paperId);
}