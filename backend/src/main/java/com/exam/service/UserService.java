package com.exam.service;

import com.exam.dto.LoginDTO;
import com.exam.dto.RegisterDTO;
import com.exam.vo.LoginVO;

public interface UserService {
    LoginVO login(LoginDTO dto);
    LoginVO register(RegisterDTO dto);
    LoginVO getProfile(Long userId);
}
