package com.exam.controller;

import com.exam.common.Result;
import com.exam.mapper.KnowledgePointMapper;
import com.exam.mapper.SubjectMapper;
import com.exam.mapper.ChapterMapper;
import com.exam.mapper.QuestionMapper;
import com.exam.mapper.UserQuestionMasteryMapper;
import com.exam.entity.*;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.exam.security.JwtAuthenticationFilter;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

@Tag(name = "知识图谱接口")
@RestController
@RequestMapping("/api/knowledge")
@RequiredArgsConstructor
public class KnowledgeController {

    private final KnowledgePointMapper knowledgePointMapper;
    private final SubjectMapper subjectMapper;
    private final ChapterMapper chapterMapper;
    private final QuestionMapper questionMapper;
    private final UserQuestionMasteryMapper masteryMapper;

    @Operation(summary = "获取知识图谱(含层级结构)")
    @GetMapping("/graph")
    public Result<?> graph(@RequestParam(defaultValue = "1") Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        List<Map<String, Object>> rows;
        if (userId != null) {
            rows = knowledgePointMapper.selectWithUserStats(userId, subjectId);
        } else {
            rows = knowledgePointMapper.selectWithUserStats(0L, subjectId);
        }
        // Load chapters for this subject
        List<Chapter> chapters = chapterMapper.selectList(
            new LambdaQueryWrapper<Chapter>().eq(Chapter::getSubjectId, subjectId).orderByAsc(Chapter::getSortOrder));
        Subject subj = subjectMapper.selectById(subjectId);
        if (subj == null) {
            return Result.success(Map.of("nodes", List.of(), "links", List.of()));
        }
        return Result.success(buildForestGraph(subj, chapters, rows, userId));
    }

    @Operation(summary = "获取薄弱知识点")
    @GetMapping("/weakness")
    public Result<?> weakness(@RequestParam(defaultValue = "1") Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        if (userId == null) return Result.success(Collections.emptyList());
        return Result.success(knowledgePointMapper.selectWeakPoints(userId, subjectId));
    }

    private Map<String, Object> buildForestGraph(Subject subj, List<Chapter> chapters,
                                                   List<Map<String, Object>> kpRows, Long userId) {
        List<Map<String, Object>> nodes = new ArrayList<>();
        List<Map<String, Object>> links = new ArrayList<>();

        String cat = subj.getName();
        String catColor = getCategoryColor(cat);

        // 1) Subject hub node (ID: negative subject ID)
        Map<String, Object> hub = new LinkedHashMap<>();
        hub.put("id", -subj.getId());
        hub.put("name", subj.getName());
        hub.put("category", cat);
        hub.put("level", "subject");
        hub.put("symbolSize", 50);
        hub.put("color", catColor);
        hub.put("doneCount", 0);
        hub.put("correctCount", 0);
        hub.put("mastery", 0);
        nodes.add(hub);

        // 2) Chapter branch nodes + links from hub
        Map<Long, Integer> chIdxMap = new HashMap<>();
        for (int c = 0; c < chapters.size(); c++) {
            Chapter ch = chapters.get(c);
            Map<String, Object> chNode = new LinkedHashMap<>();
            chNode.put("id", ch.getId());
            chNode.put("name", ch.getName());
            chNode.put("category", cat);
            chNode.put("level", "chapter");
            chNode.put("symbolSize", 32);
            chNode.put("color", catColor);
            chNode.put("doneCount", 0);
            chNode.put("correctCount", 0);
            chNode.put("mastery", 0);
            chIdxMap.put(ch.getId(), nodes.size());
            nodes.add(chNode);

            Map<String, Object> link = new LinkedHashMap<>();
            link.put("source", -subj.getId());
            link.put("target", ch.getId());
            link.put("value", "包含");
            link.put("style", "solid");
            links.add(link);
        }

        // 3) KP leaf nodes + links to chapters + inter-KP links
        Map<Long, Integer> kpIdxMap = new HashMap<>();
        Map<Long, java.util.List<Integer>> byChapter = new LinkedHashMap<>();

        for (Map<String, Object> row : kpRows) {
            Long kpId = ((Number) row.get("id")).longValue();
            Long chId = ((Number) row.get("chapter_id")).longValue();
            kpIdxMap.put(kpId, nodes.size());

            Long done = ((Number) row.getOrDefault("done_count", 0)).longValue();
            Long correct = ((Number) row.getOrDefault("correct_count", 0)).longValue();
            int mastery = done > 0 ? (int) Math.round((double) correct / done * 100) : 0;
            String mc = mastery >= 70 ? "#52c41a" : mastery >= 40 ? "#fa8c16" : mastery > 0 ? "#ff4d4f" : "#d9d9d9";

            Map<String, Object> kpNode = new LinkedHashMap<>();
            kpNode.put("id", kpId);
            kpNode.put("name", row.get("name"));
            kpNode.put("chapterId", chId);
            kpNode.put("category", cat);
            kpNode.put("level", "kp");
            kpNode.put("symbolSize", 16 + (done > 0 ? Math.min(done, 15) : 0));
            kpNode.put("color", mc);
            kpNode.put("doneCount", done);
            kpNode.put("correctCount", correct);
            kpNode.put("mastery", mastery);
            nodes.add(kpNode);

            // Link KP -> chapter
            Map<String, Object> clink = new LinkedHashMap<>();
            clink.put("source", chId);
            clink.put("target", kpId);
            clink.put("value", "属于");
            clink.put("style", "dashed");
            links.add(clink);

            // Group by chapter for inter-KP links
            byChapter.computeIfAbsent(chId, k -> new java.util.ArrayList<>()).add(kpIdxMap.get(kpId));
        }

        // Inter-KP links within same chapter (connect in pairs)
        for (java.util.List<Integer> indices : byChapter.values()) {
            for (int k = 0; k < indices.size() - 1; k++) {
                Map<String, Object> link = new LinkedHashMap<>();
                link.put("source", indices.get(k));
                link.put("target", indices.get(k + 1));
                link.put("value", "关联");
                link.put("style", "thin");
                links.add(link);
            }
        }

        // Update chapter mastery based on KPs
        for (Map.Entry<Long, Integer> e : chIdxMap.entrySet()) {
            Long chId = e.getKey();
            int total = 0, corr = 0;
            for (Map<String, Object> row : kpRows) {
                if (((Number) row.get("chapter_id")).longValue() == chId) {
                    Long d = ((Number) row.getOrDefault("done_count", 0)).longValue();
                    Long c = ((Number) row.getOrDefault("correct_count", 0)).longValue();
                    total += d; corr += c;
                }
            }
            Map<String, Object> ch = nodes.get(e.getValue());
            ch.put("doneCount", total);
            ch.put("correctCount", corr);
            ch.put("mastery", total > 0 ? (int) Math.round((double) corr / total * 100) : 0);
        }

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("nodes", nodes);
        result.put("links", links);
        return result;
    }

    private String getCategoryName(Long chapterId) {
        if (chapterId == null) return "其他";
        if (chapterId >= 101 && chapterId <= 106) return "数据结构";
        if (chapterId >= 201 && chapterId <= 206) return "计算机组成原理";
        if (chapterId >= 301 && chapterId <= 305) return "操作系统";
        if (chapterId >= 401 && chapterId <= 405) return "计算机网络";
        return "其他";
    }

    private String getCategoryColor(String name) {
        switch (name) {
            case "数据结构": return "#4f7cff";
            case "计算机组成原理": return "#fa8c16";
            case "操作系统": return "#52c41a";
            case "计算机网络": return "#9c27b0";
            default: return "#999";
        }
    }


    @Operation(summary = "获取三级知识树(科目→章节→知识点)及进度统计")
    @GetMapping("/tree")
    public Result<?> knowledgeTree(@RequestParam(defaultValue = "1") Long subjectId) {
        Long userId = JwtAuthenticationFilter.getCurrentUserId();
        
        // Load mastery data
        Map<Long, String> masteryMap = new HashMap<>();
        if (userId != null) {
            for (Map<String, Object> m : masteryMapper.selectByUserId(userId)) {
                masteryMap.put(((Number) m.get("question_id")).longValue(), (String) m.get("mastery"));
            }
        }
        
        // Get question counts per chapter and knowledge point
        List<Map<String, Object>> qStats = questionMapper.selectChapterStats();
        Map<Long, Integer> chTotalMap = new HashMap<>();
        for (Map<String, Object> s : qStats) {
            chTotalMap.put(((Number) s.get("chapter_id")).longValue(), ((Number) s.get("cnt")).intValue());
        }
        
        // Build tree: subjects -> chapters -> knowledge points
        List<Subject> subjects = subjectMapper.selectList(null);
        List<Map<String, Object>> tree = new ArrayList<>();
        
        for (Subject subj : subjects) {
            Map<String, Object> subjNode = new LinkedHashMap<>();
            subjNode.put("id", subj.getId());
            subjNode.put("name", subj.getName());
            subjNode.put("icon", subj.getIcon());
            
            List<Chapter> chapters = chapterMapper.selectList(
                new LambdaQueryWrapper<Chapter>().eq(Chapter::getSubjectId, subj.getId()).orderByAsc(Chapter::getSortOrder));
            List<Map<String, Object>> chNodes = new ArrayList<>();
            int subjTotal = 0, subjDone = 0, subjMastered = 0, subjUnfamiliar = 0, subjDontknow = 0;
            
            for (Chapter ch : chapters) {
                Map<String, Object> chNode = new LinkedHashMap<>();
                chNode.put("id", ch.getId());
                chNode.put("name", ch.getName());
                int chTotal = chTotalMap.getOrDefault(ch.getId(), 0);
                chNode.put("totalQuestions", chTotal);
                
                // Build knowledge points
                List<KnowledgePoint> kps = knowledgePointMapper.selectList(
                    new LambdaQueryWrapper<KnowledgePoint>().eq(KnowledgePoint::getChapterId, ch.getId()).orderByAsc(KnowledgePoint::getSortOrder));
                List<Map<String, Object>> kpNodes = new ArrayList<>();
                
                for (KnowledgePoint kp : kps) {
                    Map<String, Object> kpNode = new LinkedHashMap<>();
                    kpNode.put("id", kp.getId());
                    kpNode.put("name", kp.getName());
                    kpNodes.add(kpNode);
                }
                chNode.put("knowledgePoints", kpNodes);
                chNodes.add(chNode);
                subjTotal += chTotal;
            }
            
            subjNode.put("chapters", chNodes);
            subjNode.put("totalQuestions", subjTotal);
            tree.add(subjNode);
        }
        
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("tree", tree);
        return Result.success(result);
    }

}
