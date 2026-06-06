package com.exam.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.common.Result;
import com.exam.entity.KnowledgePoint;
import com.exam.mapper.ExamPaperMapper;
import com.exam.mapper.KnowledgePointMapper;
import com.exam.mapper.UserQuestionMasteryMapper;
import java.util.stream.Collectors;
import com.exam.mapper.QuestionMapper;
import com.exam.security.JwtAuthenticationFilter;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@Tag(name = "真题试卷接口")
@RestController
@RequestMapping("/api/papers")
@RequiredArgsConstructor
public class PaperController {

    private final ExamPaperMapper examPaperMapper;
    private final QuestionMapper questionMapper;
    private final KnowledgePointMapper knowledgePointMapper;
    private final UserQuestionMasteryMapper masteryMapper;

    @Operation(summary = "获取历年真题试卷列表")
    @GetMapping
    public Result<?> list(@RequestParam(defaultValue = "1") Long subjectId) {
        return Result.success(examPaperMapper.selectWithCount(subjectId));
    }

    @Operation(summary = "获取试卷题目列表")
    @GetMapping("/{paperId}/questions")
    public Result<?> questions(@PathVariable Long paperId) {
        return Result.success(examPaperMapper.selectQuestionsByPaper(paperId));
    }

    @Operation(summary = "获取真题矩阵数据（年份x题目网格+知识点树）")
    @GetMapping("/matrix")
    public Result<?> matrix(@RequestParam(defaultValue = "1") Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        List<Map<String, Object>> papers = examPaperMapper.selectWithCount(subjectId);

        // Collect all question IDs first for batch loading
        List<Long> allQuestionIds = new ArrayList<>();
        List<Map<String, Object>> years = new ArrayList<>();
        for (Map<String, Object> paper : papers) {
            Map<String, Object> yearData = new LinkedHashMap<>();
            yearData.put("year", paper.get("year"));
            yearData.put("paperId", paper.get("id"));

            List<Map<String, Object>> questions = examPaperMapper.selectQuestionsByPaper(
                ((Number) paper.get("id")).longValue());

            List<Map<String, Object>> qList = new ArrayList<>();
            for (Map<String, Object> q : questions) {
                Map<String, Object> qm = new LinkedHashMap<>();
                qm.put("questionNumber", q.get("question_number"));
                qm.put("questionId", q.get("id"));
                qm.put("chapterId", q.get("chapter_id"));
                qm.put("type", q.get("type"));
                qm.put("difficulty", q.get("difficulty"));
                qm.put("content", q.get("content"));
                qm.put("answer", q.get("answer"));
                qm.put("done", false);
                qm.put("correct", null);
                qm.put("mastery", null);
                qList.add(qm);
                allQuestionIds.add(((Number) q.get("id")).longValue());
            }
            yearData.put("questions", qList);
            years.add(yearData);
        }

        // Batch load knowledge IDs for ALL questions at once
        Map<Long, List<Long>> knowledgeIdMap = new HashMap<>();
        if (!allQuestionIds.isEmpty()) {
            List<Map<String, Object>> kpRows = questionMapper.selectKnowledgeIdsByQuestions(allQuestionIds);
            for (Map<String, Object> row : kpRows) {
                Long qid = ((Number) row.get("question_id")).longValue();
                Long kid = ((Number) row.get("knowledge_id")).longValue();
                knowledgeIdMap.computeIfAbsent(qid, k -> new ArrayList<>()).add(kid);
            }
        }
        // Assign knowledge IDs to each question
        for (Map<String, Object> yd : years) {
            for (Map<String, Object> qm : (List<Map<String, Object>>) yd.get("questions")) {
                Long qid = ((Number) qm.get("questionId")).longValue();
                qm.put("knowledgeIds", knowledgeIdMap.getOrDefault(qid, Collections.emptyList()));
            }
        }

        Map<String, Object> result = new LinkedHashMap<>();
        // Attach mastery data for logged-in user
        if (userId != null) {
            java.util.Map<Long, String> masteryMap = masteryMapper.selectByUserId(userId).stream()
                .collect(java.util.stream.Collectors.toMap(
                    m -> ((Number) m.get("question_id")).longValue(),
                    m -> (String) m.get("mastery"),
                    (a, b) -> b));
            for (Map<String, Object> yd : years) {
                for (Map<String, Object> qm : (List<Map<String, Object>>) yd.get("questions")) {
                    Long qid = ((Number) qm.get("questionId")).longValue();
                    qm.put("mastery", masteryMap.getOrDefault(qid, null));
                }
            }
        }
        result.put("years", years);
        result.put("knowledgeTree", buildKnowledgeTree(subjectId));
        return Result.success(result);
    }

        private List<Map<String, Object>> buildKnowledgeTree(Long subjectId) {
        List<KnowledgePoint> all = knowledgePointMapper.selectList(
            new LambdaQueryWrapper<KnowledgePoint>()
                .orderByAsc(KnowledgePoint::getSortOrder));
        Map<Long, List<Map<String, Object>>> byChapter = new LinkedHashMap<>();
        for (KnowledgePoint kp : all) {
            Long chId = kp.getChapterId();
            if (chId == null) continue;
            if (!byChapter.containsKey(chId)) byChapter.put(chId, new ArrayList<>());
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("id", kp.getId());
            node.put("name", kp.getName());
            byChapter.get(chId).add(node);
        }
        List<Map<String, Object>> tree = new ArrayList<>();
        long[][] ranges = {{101,106},{201,206},{301,305},{401,405}};
        String[] catNames = {"数据结构","计算机组成原理","操作系统","计算机网络"};
        String[] catIcons = {"📊","💻","⚙️","🌐"};
        for (int i = 0; i < ranges.length; i++) {
            Map<String, Object> cat = new LinkedHashMap<>();
            cat.put("name", catNames[i]);
            cat.put("icon", catIcons[i]);
            List<Map<String, Object>> children = new ArrayList<>();
            for (long ch = ranges[i][0]; ch <= ranges[i][1]; ch++) {
                if (byChapter.containsKey(ch)) children.addAll(byChapter.get(ch));
            }
            cat.put("children", children);
            tree.add(cat);
        }
        return tree;
    }
}