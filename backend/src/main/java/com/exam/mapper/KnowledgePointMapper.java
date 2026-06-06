package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.KnowledgePoint;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.util.Map;

@Mapper
public interface KnowledgePointMapper extends BaseMapper<KnowledgePoint> {

    @Select("SELECT kp.*, " +
            "COALESCE(SUM(CASE WHEN ua.is_correct = 1 THEN 1 ELSE 0 END), 0) AS correct_count, " +
            "COALESCE(COUNT(ua.id), 0) AS done_count " +
            "FROM knowledge_point kp " +
            "LEFT JOIN question_knowledge qk ON kp.id = qk.knowledge_id " +
            "LEFT JOIN user_answer ua ON qk.question_id = ua.question_id AND ua.user_id = #{userId} " +
            "WHERE kp.subject_id = #{subjectId} " +
            "GROUP BY kp.id ORDER BY kp.sort_order")
    List<Map<String, Object>> selectWithUserStats(@Param("userId") Long userId, @Param("subjectId") Long subjectId);

    @Select("SELECT kp.id, kp.name, " +
            "COUNT(qk.question_id) AS total_questions, " +
            "COALESCE(SUM(CASE WHEN ua.is_correct = 1 THEN 1 ELSE 0 END), 0) AS correct_count, " +
            "COALESCE(COUNT(DISTINCT ua.id), 0) AS done_count " +
            "FROM knowledge_point kp " +
            "LEFT JOIN question_knowledge qk ON kp.id = qk.knowledge_id " +
            "LEFT JOIN user_answer ua ON qk.question_id = ua.question_id AND ua.user_id = #{userId} " +
            "WHERE kp.subject_id = #{subjectId} " +
            "GROUP BY kp.id, kp.name " +
            "HAVING COALESCE(SUM(CASE WHEN ua.is_correct = 1 THEN 1 ELSE 0 END), 0) * 1.0 / NULLIF(COUNT(DISTINCT ua.id), 0) < 0.6 " +
            "OR COUNT(DISTINCT ua.id) = 0 " +
            "ORDER BY done_count ASC, correct_count ASC " +
            "LIMIT 10")
    List<Map<String, Object>> selectWeakPoints(@Param("userId") Long userId, @Param("subjectId") Long subjectId);
}