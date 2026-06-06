package com.exam.service.impl;

import cn.hutool.http.HttpRequest;
import cn.hutool.http.HttpResponse;
import cn.hutool.json.JSONArray;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.entity.WrongQuestion;
import com.exam.mapper.WrongQuestionMapper;
import com.exam.service.AiService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.*;

@Slf4j
@Service
public class AiServiceImpl implements AiService {

    @Value("${ai.deepseek.api-key}")
    private String apiKey;

    @Value("${ai.deepseek.base-url}")
    private String baseUrl;

    @Value("${ai.deepseek.model}")
    private String model;

    private final WrongQuestionMapper wrongQuestionMapper;

    public AiServiceImpl(WrongQuestionMapper wrongQuestionMapper) {
        this.wrongQuestionMapper = wrongQuestionMapper;
    }

    @Override
    public Map<String, Object> chat(Long userId, String question, String context) {
        String systemPrompt = buildSystemPrompt(context);
        String response = callDeepSeekApi(systemPrompt, question);

        Map<String, Object> result = new HashMap<>();
        result.put("response", response);
        return result;
    }

    @Override
    public Map<String, Object> analyzeWeakPoints(Long userId, Long subjectId) {
        List<WrongQuestion> wrongs = wrongQuestionMapper.selectList(
                new LambdaQueryWrapper<WrongQuestion>()
                        .eq(WrongQuestion::getUserId, userId)
                        .eq(WrongQuestion::getSubjectId, subjectId)
                        .eq(WrongQuestion::getIsRemoved, 0)
                        .orderByDesc(WrongQuestion::getWrongCount)
                        .last("LIMIT 20")
        );

        if (wrongs.isEmpty()) {
            Map<String, Object> result = new HashMap<>();
            result.put("response", "暂无足够错题数据，继续刷题积累数据后可以为你分析薄弱环节。");
            return result;
        }

        String analysisPrompt = "用户在该科目下共有" + wrongs.size() + "道错题。请分析可能存在哪些薄弱知识点，并给出针对性学习建议。";
        String response = callDeepSeekApi(
                "你是考研辅导专家，擅长分析学生薄弱环节并给出针对性学习建议。用中文回答，条理清晰。",
                analysisPrompt
        );

        Map<String, Object> result = new HashMap<>();
        result.put("response", response);
        result.put("wrongCount", wrongs.size());
        return result;
    }

    private String buildSystemPrompt(String context) {
        return "你是专业的考研辅导AI助手，精通408计算机综合和高等数学。" +
               "以通俗易懂的方式帮助用户理解题目和知识点，分步骤讲解，举例子说明。" +
               (context != null && !context.isEmpty() ? "当前题目上下文：" + context : "");
    }

    private String callDeepSeekApi(String systemPrompt, String userMessage) {
        try {
            JSONObject body = new JSONObject();
            body.put("model", model);
            body.put("stream", false);

            JSONArray messages = new JSONArray();

            JSONObject sysMsg = new JSONObject();
            sysMsg.put("role", "system");
            sysMsg.put("content", systemPrompt);
            messages.add(sysMsg);

            JSONObject userMsg = new JSONObject();
            userMsg.put("role", "user");
            userMsg.put("content", userMessage);
            messages.add(userMsg);

            body.put("messages", messages);
            body.put("temperature", 0.7);
            body.put("max_tokens", 2000);

            HttpResponse response = HttpRequest.post(baseUrl + "/v1/chat/completions")
                    .header("Authorization", "Bearer " + apiKey)
                    .header("Content-Type", "application/json")
                    .body(body.toString())
                    .timeout(60000)
                    .execute();

            if (response.getStatus() == 200) {
                JSONObject respJson = JSONUtil.parseObj(response.body());
                JSONArray choices = respJson.getJSONArray("choices");
                if (choices != null && !choices.isEmpty()) {
                    return choices.getJSONObject(0)
                            .getJSONObject("message")
                            .getStr("content", "AI暂时无法回答。");
                }
            }

            log.error("DeepSeek API error: status={}", response.getStatus());
            return "AI服务暂时不可用，请稍后再试。";
        } catch (Exception e) {
            log.error("Call DeepSeek API failed", e);
            return "AI服务调用失败，请检查API配置。";
        }
    }
}
