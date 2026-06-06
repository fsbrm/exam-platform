package com.exam.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.common.BusinessException;
import com.exam.dto.LoginDTO;
import com.exam.dto.RegisterDTO;
import com.exam.entity.InviteCode;
import com.exam.entity.User;
import com.exam.mapper.InviteCodeMapper;
import com.exam.mapper.UserMapper;
import com.exam.security.JwtUtils;
import com.exam.service.UserService;
import com.exam.vo.LoginVO;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserMapper userMapper;
    private final InviteCodeMapper inviteCodeMapper;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtils jwtUtils;

    @Override
    public LoginVO login(LoginDTO dto) {
        User user = userMapper.selectOne(
                new LambdaQueryWrapper<User>().eq(User::getUsername, dto.getUsername())
        );
        if (user == null || !passwordEncoder.matches(dto.getPassword(), user.getPassword())) {
            throw new BusinessException(401, "用户名或密码错误");
        }
        if (user.getStatus() != null && user.getStatus() == 0) {
            throw new BusinessException(403, "账号已被禁用");
        }
        String token = jwtUtils.generateToken(user.getId(), user.getUsername(), user.getRole());
        return buildLoginVO(user, token);
    }

    @Override
    @Transactional
    public LoginVO register(RegisterDTO dto) {
        // Validate invite code
        InviteCode inviteCode = inviteCodeMapper.selectOne(
                new LambdaQueryWrapper<InviteCode>().eq(InviteCode::getCode, dto.getInviteCode())
        );
        if (inviteCode == null) {
            throw new BusinessException("邀请码无效");
        }
        if (inviteCode.getUsed() != null && inviteCode.getUsed() == 1) {
            throw new BusinessException("邀请码已被使用");
        }

        Long count = userMapper.selectCount(
                new LambdaQueryWrapper<User>().eq(User::getUsername, dto.getUsername())
        );
        if (count > 0) {
            throw new BusinessException("用户名已存在");
        }

        User user = new User();
        user.setUsername(dto.getUsername());
        user.setPassword(passwordEncoder.encode(dto.getPassword()));
        user.setEmail(dto.getEmail());
        user.setNickname(dto.getNickname() != null ? dto.getNickname() : dto.getUsername());
        user.setRole("USER");
        user.setStatus(1);
        userMapper.insert(user);

        // Mark invite code as used
        inviteCode.setUsed(1);
        inviteCode.setUsedBy(user.getId());
        inviteCode.setUsedAt(LocalDateTime.now());
        inviteCodeMapper.updateById(inviteCode);

        String token = jwtUtils.generateToken(user.getId(), user.getUsername(), user.getRole());
        return buildLoginVO(user, token);
    }

    @Override
    public LoginVO getProfile(Long userId) {
        User user = userMapper.selectById(userId);
        if (user == null) {
            throw new BusinessException("用户不存在");
        }
        return buildLoginVO(user, null);
    }

    private LoginVO buildLoginVO(User user, String token) {
        return LoginVO.builder()
                .token(token)
                .userId(user.getId())
                .username(user.getUsername())
                .nickname(user.getNickname())
                .avatar(user.getAvatar())
                .role(user.getRole())
                .build();
    }
}