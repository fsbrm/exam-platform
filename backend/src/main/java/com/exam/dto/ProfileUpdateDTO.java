package com.exam.dto;

import jakarta.validation.constraints.Email;
import lombok.Data;

@Data
public class ProfileUpdateDTO {
    private String nickname;

    @Email(message = "邮箱格式不正确")
    private String email;

    private String avatar;
}