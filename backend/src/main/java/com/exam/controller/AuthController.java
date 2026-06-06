package com.exam.controller;

import com.exam.common.Result;
import com.exam.dto.LoginDTO;
import com.exam.dto.RegisterDTO;
import com.exam.security.JwtAuthenticationFilter;
import com.exam.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@Tag(name = "认证接口")
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserService userService;

    @Operation(summary = "登录")
    @PostMapping("/login")
    public Result<?> login(@Valid @RequestBody LoginDTO dto) {
        return Result.success(userService.login(dto));
    }

    @Operation(summary = "注册")
    @PostMapping("/register")
    public Result<?> register(@Valid @RequestBody RegisterDTO dto) {
        return Result.success(userService.register(dto));
    }

    @Operation(summary = "获取个人信息")
    @GetMapping("/profile")
    public Result<?> profile() {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.error(401, "未登录");
        return Result.success(userService.getProfile(userId));
    }
}
