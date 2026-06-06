import os

# Map question numbers to knowledge points
# knowledge_point IDs: 1-43 (as inserted earlier)
# Q# ranges for knowledge points (rough mapping based on subject areas)

q_to_kp = {
    # Data Structure (Q1-11) -> kp 1-13
    1: [1], 2: [1,2], 3: [3], 4: [3,4], 5: [5,6], 6: [5], 7: [5,7], 8: [8],
    9: [8,9], 10: [10], 11: [12,13],
    # Computer Organization (Q12-22) -> kp 14-23
    12: [14,15], 13: [14], 14: [15], 15: [16], 16: [16,17], 17: [17],
    18: [18,19], 19: [18], 20: [20], 21: [20,21], 22: [22,23],
    # Operating System (Q23-32) -> kp 24-31
    23: [24], 24: [24], 25: [25], 26: [26], 27: [26,27], 28: [28],
    29: [28,29], 30: [30,31], 31: [31], 32: [24,25],
    # Computer Network (Q33-40) -> kp 32-43
    33: [32,33], 34: [34,35], 35: [34], 36: [36,37], 37: [36],
    38: [38,39], 39: [38], 40: [40,41,42,43],
}

output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "link_kp.sql")
lines = ["USE exam_platform;", "", "DELETE FROM question_knowledge;", "",
         "INSERT INTO question_knowledge (question_id, knowledge_id) VALUES"]

rows = []
# For each question, link to knowledge points based on question number
# Questions are numbered 1-40 per year, ID ranges by year
# Year 2009: IDs 1-37, 2010: 38-74, etc.
# We need actual question IDs from DB

# Generate a query that links based on question chapter_id (which equals question number)
lines = [
    "USE exam_platform;",
    "",
    "DELETE FROM question_knowledge;",
    "",
    "-- Link questions to knowledge points based on question number (chapter_id = question number 1-40)",
    "-- DS: Q1-11, CO: Q12-22, OS: Q23-32, CN: Q33-40",
    "",
    "-- Data Structure (Q1-11): knowledge points 1-13",
    "INSERT INTO question_knowledge (question_id, knowledge_id)",
    "SELECT q.id, CASE",
    "  WHEN q.chapter_id = 1 THEN 1",
    "  WHEN q.chapter_id = 2 THEN 2",
    "  WHEN q.chapter_id = 3 THEN 3",
    "  WHEN q.chapter_id = 4 THEN 4",
    "  WHEN q.chapter_id = 5 THEN 5",
    "  WHEN q.chapter_id = 6 THEN 6",
    "  WHEN q.chapter_id = 7 THEN 7",
    "  WHEN q.chapter_id = 8 THEN 8",
    "  WHEN q.chapter_id = 9 THEN 9",
    "  WHEN q.chapter_id = 10 THEN 10",
    "  WHEN q.chapter_id = 11 THEN 13",
    "END",
    "FROM question q WHERE q.chapter_id BETWEEN 1 AND 11;",
    "",
    "-- Computer Organization (Q12-22): knowledge points 14-23",
    "INSERT INTO question_knowledge (question_id, knowledge_id)",
    "SELECT q.id, CASE",
    "  WHEN q.chapter_id = 12 THEN 15",
    "  WHEN q.chapter_id = 13 THEN 15",
    "  WHEN q.chapter_id = 14 THEN 15",
    "  WHEN q.chapter_id = 15 THEN 16",
    "  WHEN q.chapter_id = 16 THEN 16",
    "  WHEN q.chapter_id = 17 THEN 17",
    "  WHEN q.chapter_id = 18 THEN 18",
    "  WHEN q.chapter_id = 19 THEN 19",
    "  WHEN q.chapter_id = 20 THEN 20",
    "  WHEN q.chapter_id = 21 THEN 21",
    "  WHEN q.chapter_id = 22 THEN 22",
    "END",
    "FROM question q WHERE q.chapter_id BETWEEN 12 AND 22;",
    "",
    "-- Operating System (Q23-32): knowledge points 24-31",
    "INSERT INTO question_knowledge (question_id, knowledge_id)",
    "SELECT q.id, CASE",
    "  WHEN q.chapter_id = 23 THEN 24",
    "  WHEN q.chapter_id = 24 THEN 24",
    "  WHEN q.chapter_id = 25 THEN 25",
    "  WHEN q.chapter_id = 26 THEN 26",
    "  WHEN q.chapter_id = 27 THEN 27",
    "  WHEN q.chapter_id = 28 THEN 28",
    "  WHEN q.chapter_id = 29 THEN 29",
    "  WHEN q.chapter_id = 30 THEN 30",
    "  WHEN q.chapter_id = 31 THEN 31",
    "  WHEN q.chapter_id = 32 THEN 24",
    "END",
    "FROM question q WHERE q.chapter_id BETWEEN 23 AND 32;",
    "",
    "-- Computer Network (Q33-40): knowledge points 32-43",
    "INSERT INTO question_knowledge (question_id, knowledge_id)",
    "SELECT q.id, CASE",
    "  WHEN q.chapter_id = 33 THEN 33",
    "  WHEN q.chapter_id = 34 THEN 34",
    "  WHEN q.chapter_id = 35 THEN 35",
    "  WHEN q.chapter_id = 36 THEN 36",
    "  WHEN q.chapter_id = 37 THEN 37",
    "  WHEN q.chapter_id = 38 THEN 38",
    "  WHEN q.chapter_id = 39 THEN 39",
    "  WHEN q.chapter_id = 40 THEN 40",
    "END",
    "FROM question q WHERE q.chapter_id BETWEEN 33 AND 40;",
]

with open(output, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Generated {output}")