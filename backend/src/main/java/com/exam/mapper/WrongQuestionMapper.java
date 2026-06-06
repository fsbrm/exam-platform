package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.WrongQuestion;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.util.Map;

@Mapper
public interface WrongQuestionMapper extends BaseMapper<WrongQuestion> {

    @Select("SELECT wq.*, q.content, q.type, q.difficulty, q.chapter_id, " +
            "c.name as chapter_name, s.name as subject_name " +
            "FROM wrong_question wq " +
            "LEFT JOIN question q ON wq.question_id = q.id " +
            "LEFT JOIN chapter c ON q.chapter_id = c.id " +
            "LEFT JOIN subject s ON wq.subject_id = s.id " +
            "WHERE wq.user_id = #{userId} AND wq.is_removed = 0 " +
            "ORDER BY wq.last_wrong_at DESC")
    List<WrongQuestion> selectByUserWithDetail(@Param("userId") Long userId);

    @Select("SELECT wq.id, wq.question_id, wq.wrong_count, wq.last_wrong_at, wq.subject_id, " +
            "q.content, q.type, q.difficulty, q.chapter_id, q.answer, q.analysis, " +
            "c.name as chapter_name, s.name as subject_name, " +
            "COALESCE(m.mastery, '') as mastery, " +
            "CASE WHEN f.id IS NOT NULL THEN 1 ELSE 0 END as is_favorited " +
            "FROM wrong_question wq " +
            "INNER JOIN question q ON wq.question_id = q.id " +
            "LEFT JOIN chapter c ON q.chapter_id = c.id " +
            "LEFT JOIN subject s ON wq.subject_id = s.id " +
            "LEFT JOIN user_question_mastery m ON wq.question_id = m.question_id AND wq.user_id = m.user_id " +
            "LEFT JOIN favorite f ON wq.question_id = f.question_id AND wq.user_id = f.user_id " +
            "WHERE wq.user_id = #{userId} AND wq.is_removed = 0 " +
            "ORDER BY wq.last_wrong_at DESC")
    List<Map<String, Object>> selectEnhancedAll(@Param("userId") Long userId);
}
