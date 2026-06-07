package com.exam.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.exam.entity.InviteCode;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface InviteCodeMapper extends BaseMapper<InviteCode> {

    @Select("SELECT id, code, used, used_at as usedAt, created_at as createdAt, created_by as createdBy, used_by as usedBy FROM invite_code ORDER BY created_at DESC LIMIT #{limit} OFFSET #{offset}")
    List<Map<String, Object>> pageQuery(@Param("limit") int limit, @Param("offset") int offset);

    @Select("SELECT COUNT(*) FROM invite_code")
    long countAll();

    @Select("SELECT COUNT(*) FROM invite_code WHERE used = 0")
    long countUnused();
}