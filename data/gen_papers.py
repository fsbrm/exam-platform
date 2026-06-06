import os

# Generate SQL to create exam papers and link questions
output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "papers_data.sql")

lines = [
    "USE exam_platform;",
    "",
    "-- Clear existing papers",
    "DELETE FROM paper_question;",
    "DELETE FROM exam_paper;",
    "ALTER TABLE exam_paper AUTO_INCREMENT = 1;",
    "",
    "-- Insert exam papers (2009-2021)",
]

paper_id = 1
paper_questions = []

for year in range(2009, 2022):
    lines.append(f"INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES ({paper_id}, 1, {year}, '{year}年408计算机基础综合真题', 150, 180, 47);")
    
    # Find question IDs for this year
    # Questions are inserted sequentially by year
    paper_questions.append(f"-- Year {year} questions will be linked by query below")
    paper_id += 1

lines.append("")
lines.append("-- Link questions to papers based on year")
lines.append("INSERT INTO paper_question (paper_id, question_id, sort_order)")
lines.append("SELECT ep.id, q.id, q.id - (SELECT MIN(id) FROM question WHERE year = ep.year) + 1")
lines.append("FROM exam_paper ep")
lines.append("JOIN question q ON q.year = ep.year")
lines.append("ORDER BY ep.year, q.id;")

with open(output, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Generated {output}")