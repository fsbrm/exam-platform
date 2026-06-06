package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.UserQuestionMastery;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import java.util.List;
import java.util.Map;

@Mapper
public interface UserQuestionMasteryMapper extends BaseMapper<UserQuestionMastery> {
    
    @Select("SELECT question_id, mastery FROM user_question_mastery WHERE user_id = #{userId}")
    List<Map<String, Object>> selectByUserId(@Param("userId") Long userId);
}