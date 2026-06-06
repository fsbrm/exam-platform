package com.exam.service;

import com.exam.entity.Favorite;
import java.util.List;

public interface FavoriteService {
    void toggle(Long userId, Long questionId);
    List<Favorite> listByUser(Long userId);
    boolean isFavorited(Long userId, Long questionId);
}
