package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.WrongQuestion;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import java.util.List;

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

    @Select("<script>" +
            "SELECT wq.id, wq.question_id, wq.wrong_count, wq.last_wrong_at, wq.subject_id, " +
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
            "<if test='subjectId != null'>AND wq.subject_id = #{subjectId}</if> " +
            "<if test='chapterId != null'>AND q.chapter_id = #{chapterId}</if> " +
            "<if test='mastery != null and mastery != \"\"'>AND m.mastery = #{mastery}</if> " +
            "<if test='favoriteOnly != null and favoriteOnly == true'>AND f.id IS NOT NULL</if> " +
            "<if test='yearMonth != null and yearMonth != \"\"'>AND DATE_FORMAT(wq.last_wrong_at, '%Y-%m') = #{yearMonth}</if> " +
            "ORDER BY wq.last_wrong_at DESC" +
            "</script>")
    List<Map<String, Object>> selectEnhanced(@Param("userId") Long userId,
                                             @Param("subjectId") Long subjectId,
                                             @Param("chapterId") Long chapterId,
                                             @Param("mastery") String mastery,
                                             @Param("favoriteOnly") Boolean favoriteOnly,
                                             @Param("yearMonth") String yearMonth);
}
