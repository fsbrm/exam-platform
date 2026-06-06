package com.exam.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.entity.Favorite;
import com.exam.mapper.FavoriteMapper;
import com.exam.service.FavoriteService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class FavoriteServiceImpl implements FavoriteService {

    private final FavoriteMapper favoriteMapper;

    @Override
    @Transactional
    public void toggle(Long userId, Long questionId) {
        Favorite fav = favoriteMapper.selectOne(
                new LambdaQueryWrapper<Favorite>()
                        .eq(Favorite::getUserId, userId)
                        .eq(Favorite::getQuestionId, questionId)
        );
        if (fav == null) {
            fav = new Favorite();
            fav.setUserId(userId);
            fav.setQuestionId(questionId);
            fav.setCreatedAt(LocalDateTime.now());
            favoriteMapper.insert(fav);
        } else {
            favoriteMapper.deleteById(fav.getId());
        }
    }

    @Override
    public List<Favorite> listByUser(Long userId) {
        return favoriteMapper.selectList(
                new LambdaQueryWrapper<Favorite>()
                        .eq(Favorite::getUserId, userId)
                        .orderByDesc(Favorite::getCreatedAt)
        );
    }

    @Override
    public boolean isFavorited(Long userId, Long questionId) {
        return favoriteMapper.selectCount(
                new LambdaQueryWrapper<Favorite>()
                        .eq(Favorite::getUserId, userId)
                        .eq(Favorite::getQuestionId, questionId)
        ) > 0;
    }
}
