import os, re

file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "src", "main", "java", "com", "exam", "controller", "KnowledgeController.java"))
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
old_import = "import com.exam.mapper.KnowledgePointMapper;"
new_import = "import com.exam.mapper.KnowledgePointMapper;\nimport com.exam.mapper.SubjectMapper;\nimport com.exam.mapper.ChapterMapper;\nimport com.exam.mapper.QuestionMapper;\nimport com.exam.mapper.UserQuestionMasteryMapper;\nimport com.exam.entity.*;\nimport com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;"
content = content.replace(old_import, new_import)

# Add mappers
old_field = "private final KnowledgePointMapper knowledgePointMapper;"
new_field = "private final KnowledgePointMapper knowledgePointMapper;\n    private final SubjectMapper subjectMapper;\n    private final ChapterMapper chapterMapper;\n    private final QuestionMapper questionMapper;\n    private final UserQuestionMasteryMapper masteryMapper;"
content = content.replace(old_field, new_field)

# Add tree endpoint before the closing brace of the class
# Find the last } and insert before it
last_brace = content.rfind('}')
endpoint = '''

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
'''

content = content[:last_brace] + endpoint + "\n}\n"

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Knowledge tree API added")