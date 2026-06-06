package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.WrongQuestion;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface WrongQuestionMapper extends BaseMapper<WrongQuestion> {

    @Select("SELECT wq.*, q.content, q.type, q.difficulty, c.name as chapter_name, s.name as subject_name " +
            "FROM wrong_question wq " +
            "LEFT JOIN question q ON wq.question_id = q.id " +
            "LEFT JOIN chapter c ON q.chapter_id = c.id " +
            "LEFT JOIN subject s ON wq.subject_id = s.id " +
            "WHERE wq.user_id = #{userId} AND wq.is_removed = 0 " +
            "ORDER BY wq.last_wrong_at DESC")
    List<WrongQuestion> selectByUserWithDetail(@Param("userId") Long userId);
}
