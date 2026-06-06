package com.exam.dto;

import jakarta.validation.constraints.Email;
import lombok.Data;

@Data
public class ProfileUpdateDTO {
    private String nickname;

    @Email(message = "Invalid email format")
    private String email;

    private String avatar;
}