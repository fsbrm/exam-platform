fp = r'D:\桌面\毕设\exam-platform\backend\src\main\java\com\exam\mapper\QuestionMapper.java'
with open(fp, 'r', encoding='utf-8') as f:
    c = f.read()

# Remove trailing } and add method
c = c.rstrip()
if c.endswith('}'):
    c = c[:-1].rstrip()
    c += '\n\n    @Select("SELECT pq.question_number FROM paper_question pq WHERE pq.question_id = #{questionId} LIMIT 1")\n    Integer selectQuestionNumber(@Param("questionId") Long questionId);\n}\n'

with open(fp, 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
