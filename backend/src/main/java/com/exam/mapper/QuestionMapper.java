package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.Question;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.util.Map;

@Mapper
public interface QuestionMapper extends BaseMapper<Question> {

    @Select("SELECT q.*, pq.question_number as questionNumber FROM question q LEFT JOIN paper_question pq ON q.id = pq.question_id WHERE q.subject_id = #{subjectId} AND q.status = 1 ORDER BY q.year, pq.question_number")
    List<Question> selectBySubject(@Param("subjectId") Long subjectId);

    @Select("SELECT q.*, pq.question_number as questionNumber FROM question q LEFT JOIN paper_question pq ON q.id = pq.question_id WHERE q.subject_id = #{subjectId} AND q.status = 1 ORDER BY RAND() LIMIT #{count}")
    List<Question> selectRandomBySubject(@Param("subjectId") Long subjectId, @Param("count") int count);

    @Select("SELECT * FROM question WHERE chapter_id = #{chapterId} AND status = 1 ORDER BY id")
    List<Question> selectByChapter(@Param("chapterId") Long chapterId);

    @Select("SELECT knowledge_id FROM question_knowledge WHERE question_id = #{questionId}")
    List<Long> selectKnowledgeIdsByQuestion(@Param("questionId") Long questionId);

    @Select("SELECT DISTINCT q.*, pq.question_number as questionNumber FROM question q INNER JOIN question_knowledge qk ON q.id = qk.question_id LEFT JOIN paper_question pq ON q.id = pq.question_id WHERE qk.knowledge_id = #{knowledgeId} AND q.status = 1 ORDER BY q.year, pq.question_number")
    List<Question> selectByKnowledgeId(@Param("knowledgeId") Long knowledgeId);

    @Select("SELECT chapter_id, COUNT(*) as cnt FROM question WHERE status = 1 AND chapter_id >= 100 GROUP BY chapter_id")
    List<Map<String, Object>> selectChapterStats();

    @Select("SELECT pq.question_number FROM paper_question pq WHERE pq.question_id = #{questionId} LIMIT 1")
    Integer selectQuestionNumber(@Param("questionId") Long questionId);

    @Select("SELECT q.*, pq.question_number as questionNumber FROM question q LEFT JOIN paper_question pq ON q.id = pq.question_id WHERE q.year = #{year} AND q.status = 1 ORDER BY pq.question_number")
    List<Question> selectByYear(@Param("year") Integer year);

    @Select("SELECT q.*, pq.question_number as questionNumber FROM question q LEFT JOIN paper_question pq ON q.id = pq.question_id WHERE q.status = 1 ORDER BY q.year, pq.question_number")
    List<Question> selectAll();
}
