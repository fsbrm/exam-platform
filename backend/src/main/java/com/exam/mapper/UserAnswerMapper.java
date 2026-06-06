package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.UserAnswer;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Mapper
public interface UserAnswerMapper extends BaseMapper<UserAnswer> {

    @Select("SELECT COUNT(*) FROM user_answer WHERE user_id = #{userId} AND DATE(answered_at) = CURDATE()")
    Long countTodayByUser(@Param("userId") Long userId);

    @Select("SELECT COUNT(*) FROM user_answer WHERE user_id = #{userId} AND is_correct = 1 AND DATE(answered_at) = CURDATE()")
    Long countTodayCorrectByUser(@Param("userId") Long userId);

    @Select("SELECT COUNT(*) FROM user_answer WHERE user_id = #{userId}")
    Long countByUser(@Param("userId") Long userId);

    @Select("SELECT COUNT(*) FROM user_answer WHERE user_id = #{userId} AND is_correct = 1")
    Long countCorrectByUser(@Param("userId") Long userId);

    @Select("SELECT COUNT(DISTINCT DATE(answered_at)) FROM user_answer WHERE user_id = #{userId}")
    Integer countStudyDays(@Param("userId") Long userId);

    @Select("SELECT DATE(answered_at) as date, COUNT(*) as count FROM user_answer " +
            "WHERE user_id = #{userId} AND answered_at >= #{startDate} " +
            "GROUP BY DATE(answered_at) ORDER BY date")
    List<Map<String, Object>> dailyCount(@Param("userId") Long userId, @Param("startDate") LocalDate startDate);

    @Select("SELECT DATE(answered_at) as date, COUNT(*) as total, " +
            "SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct " +
            "FROM user_answer WHERE user_id = #{userId} AND answered_at >= #{startDate} " +
            "GROUP BY DATE(answered_at) ORDER BY date")
    List<Map<String, Object>> dailyStats(@Param("userId") Long userId, @Param("startDate") LocalDate startDate);

    @Select("SELECT s.name as name, " +
            "COUNT(ua.id) as doneCount, " +
            "SUM(CASE WHEN ua.is_correct = 1 THEN 1 ELSE 0 END) as correctCount, " +
            "(SELECT COUNT(*) FROM question q WHERE q.subject_id = s.id AND q.status = 1) as totalCount " +
            "FROM user_answer ua " +
            "LEFT JOIN subject s ON ua.subject_id = s.id " +
            "WHERE ua.user_id = #{userId} " +
            "GROUP BY ua.subject_id, s.name")
    List<Map<String, Object>> subjectStats(@Param("userId") Long userId);

    @Select("SELECT COUNT(*) FROM user_answer WHERE user_id = #{userId} AND subject_id = #{subjectId}")
    Long countByUserAndSubject(@Param("userId") Long userId, @Param("subjectId") Long subjectId);

    @Select("SELECT COUNT(*) FROM user_answer WHERE user_id = #{userId} AND subject_id = #{subjectId} AND is_correct = 1")
    Long countCorrectByUserAndSubject(@Param("userId") Long userId, @Param("subjectId") Long subjectId);

    @Select("SELECT COUNT(DISTINCT DATE(answered_at)) FROM user_answer WHERE user_id = #{userId} AND subject_id = #{subjectId}")
    Integer countStudyDaysBySubject(@Param("userId") Long userId, @Param("subjectId") Long subjectId);

    @Select("SELECT DATE(answered_at) as date, COUNT(*) as count FROM user_answer " +
            "WHERE user_id = #{userId} AND subject_id = #{subjectId} AND answered_at >= #{startDate} " +
            "GROUP BY DATE(answered_at) ORDER BY date")
    List<Map<String, Object>> dailyCountBySubject(@Param("userId") Long userId, @Param("subjectId") Long subjectId, @Param("startDate") LocalDate startDate);

    @Select("SELECT DATE(answered_at) as date, COUNT(*) as total, " +
            "SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct " +
            "FROM user_answer WHERE user_id = #{userId} AND subject_id = #{subjectId} AND answered_at >= #{startDate} " +
            "GROUP BY DATE(answered_at) ORDER BY date")
    List<Map<String, Object>> dailyStatsBySubject(@Param("userId") Long userId, @Param("subjectId") Long subjectId, @Param("startDate") LocalDate startDate);

    @Select("SELECT c.id as chapterId, c.name as chapterName, " +
            "COUNT(ua.id) as doneCount, " +
            "SUM(CASE WHEN ua.is_correct = 1 THEN 1 ELSE 0 END) as correctCount, " +
            "(SELECT COUNT(*) FROM question q WHERE q.chapter_id = c.id AND q.status = 1) as totalCount " +
            "FROM chapter c " +
            "LEFT JOIN user_answer ua ON c.id = (SELECT q2.chapter_id FROM question q2 WHERE q2.id = ua.question_id) AND ua.user_id = #{userId} " +
            "WHERE c.subject_id = #{subjectId} AND c.parent_id > 0 " +
            "GROUP BY c.id, c.name ORDER BY c.sort_order")
    List<Map<String, Object>> chapterMasteryBySubject(@Param("userId") Long userId, @Param("subjectId") Long subjectId);

    // ─── Admin Analytics ───

    @Select("SELECT COUNT(*) FROM user_answer WHERE DATE(answered_at) = CURDATE()")
    Long countTodayTotal();

    @Select("SELECT COUNT(DISTINCT user_id) FROM user_answer WHERE DATE(answered_at) = CURDATE()")
    Long countTodayActiveUsers();

    @Select("SELECT u.id, u.username, u.nickname, MAX(ua.answered_at) as last_active " +
            "FROM user_answer ua JOIN user u ON ua.user_id = u.id " +
            "WHERE ua.answered_at >= #{since} GROUP BY u.id, u.username, u.nickname ORDER BY last_active DESC")
    List<Map<String, Object>> getOnlineUsers(@Param("since") LocalDateTime since);

    @Select("SELECT DATE(answered_at) as date, COUNT(DISTINCT user_id) as count " +
            "FROM user_answer WHERE answered_at >= DATE_SUB(CURDATE(), INTERVAL #{days} DAY) " +
            "GROUP BY DATE(answered_at) ORDER BY date")
    List<Map<String, Object>> dailyActiveUsers(@Param("days") int days);

    @Select("SELECT DATE(answered_at) as date, COUNT(*) as count " +
            "FROM user_answer WHERE answered_at >= DATE_SUB(CURDATE(), INTERVAL #{days} DAY) " +
            "GROUP BY DATE(answered_at) ORDER BY date")
    List<Map<String, Object>> dailyPracticeCount(@Param("days") int days);

    @Select("SELECT COUNT(DISTINCT user_id) FROM user_answer " +
            "WHERE answered_at >= #{start} AND answered_at < #{end}")
    Long countActiveBetween(@Param("start") LocalDateTime start, @Param("end") LocalDateTime end);

    @Select("SELECT u.id, u.username, u.nickname, COUNT(*) as cnt " +
            "FROM user_answer ua JOIN user u ON ua.user_id = u.id " +
            "WHERE DATE(ua.answered_at) = CURDATE() " +
            "GROUP BY u.id, u.username, u.nickname ORDER BY cnt DESC LIMIT #{limit}")
    List<Map<String, Object>> dailyTopUsers(@Param("limit") int limit);

    @Select("SELECT u.id, u.username, u.nickname, COUNT(*) as cnt " +
            "FROM user_answer ua JOIN user u ON ua.user_id = u.id " +
            "GROUP BY u.id, u.username, u.nickname ORDER BY cnt DESC LIMIT #{limit}")
    List<Map<String, Object>> totalTopUsers(@Param("limit") int limit);

    @Select("SELECT s.name, COUNT(*) as cnt FROM user_answer ua " +
            "JOIN subject s ON ua.subject_id = s.id GROUP BY ua.subject_id, s.name")
    List<Map<String, Object>> subjectDistribution();

    @Select("SELECT ua.question_id as questionId, q.content, q.subject_id, s.name as subjectName, " +
            "ua.answered_at as answeredAt, ua.user_answer as userAnswer, ua.is_correct as isCorrect " +
            "FROM user_answer ua JOIN question q ON ua.question_id = q.id " +
            "LEFT JOIN subject s ON q.subject_id = s.id " +
            "WHERE ua.user_id = #{userId} ORDER BY ua.answered_at DESC LIMIT #{limit}")
    List<Map<String, Object>> selectRecentByUser(@Param("userId") Long userId, @Param("limit") int limit);

    @Select("SELECT MAX(answered_at) as answered_at FROM user_answer WHERE user_id = #{userId}")
    Map<String, Object> selectLastActive(@Param("userId") Long userId);
}
