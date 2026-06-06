fp = r'D:\桌面\毕设\exam-platform\backend\src\main\java\com\exam\mapper\QuestionMapper.java'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

# Add method before the closing brace
new_method = '''
    @Select("SELECT pq.question_number FROM paper_question pq WHERE pq.question_id = #{questionId} LIMIT 1")
    Integer selectQuestionNumber(@Param("questionId") Long questionId);
}
'''
c = c.replace('}\n', new_method)
with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('QuestionMapper updated')
