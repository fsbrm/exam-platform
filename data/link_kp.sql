USE exam_platform;

DELETE FROM question_knowledge;

-- Link questions to knowledge points based on question number (chapter_id = question number 1-40)
-- DS: Q1-11, CO: Q12-22, OS: Q23-32, CN: Q33-40

-- Data Structure (Q1-11): knowledge points 1-13
INSERT INTO question_knowledge (question_id, knowledge_id)
SELECT q.id, CASE
  WHEN q.chapter_id = 1 THEN 1
  WHEN q.chapter_id = 2 THEN 2
  WHEN q.chapter_id = 3 THEN 3
  WHEN q.chapter_id = 4 THEN 4
  WHEN q.chapter_id = 5 THEN 5
  WHEN q.chapter_id = 6 THEN 6
  WHEN q.chapter_id = 7 THEN 7
  WHEN q.chapter_id = 8 THEN 8
  WHEN q.chapter_id = 9 THEN 9
  WHEN q.chapter_id = 10 THEN 10
  WHEN q.chapter_id = 11 THEN 13
END
FROM question q WHERE q.chapter_id BETWEEN 1 AND 11;

-- Computer Organization (Q12-22): knowledge points 14-23
INSERT INTO question_knowledge (question_id, knowledge_id)
SELECT q.id, CASE
  WHEN q.chapter_id = 12 THEN 15
  WHEN q.chapter_id = 13 THEN 15
  WHEN q.chapter_id = 14 THEN 15
  WHEN q.chapter_id = 15 THEN 16
  WHEN q.chapter_id = 16 THEN 16
  WHEN q.chapter_id = 17 THEN 17
  WHEN q.chapter_id = 18 THEN 18
  WHEN q.chapter_id = 19 THEN 19
  WHEN q.chapter_id = 20 THEN 20
  WHEN q.chapter_id = 21 THEN 21
  WHEN q.chapter_id = 22 THEN 22
END
FROM question q WHERE q.chapter_id BETWEEN 12 AND 22;

-- Operating System (Q23-32): knowledge points 24-31
INSERT INTO question_knowledge (question_id, knowledge_id)
SELECT q.id, CASE
  WHEN q.chapter_id = 23 THEN 24
  WHEN q.chapter_id = 24 THEN 24
  WHEN q.chapter_id = 25 THEN 25
  WHEN q.chapter_id = 26 THEN 26
  WHEN q.chapter_id = 27 THEN 27
  WHEN q.chapter_id = 28 THEN 28
  WHEN q.chapter_id = 29 THEN 29
  WHEN q.chapter_id = 30 THEN 30
  WHEN q.chapter_id = 31 THEN 31
  WHEN q.chapter_id = 32 THEN 24
END
FROM question q WHERE q.chapter_id BETWEEN 23 AND 32;

-- Computer Network (Q33-40): knowledge points 32-43
INSERT INTO question_knowledge (question_id, knowledge_id)
SELECT q.id, CASE
  WHEN q.chapter_id = 33 THEN 33
  WHEN q.chapter_id = 34 THEN 34
  WHEN q.chapter_id = 35 THEN 35
  WHEN q.chapter_id = 36 THEN 36
  WHEN q.chapter_id = 37 THEN 37
  WHEN q.chapter_id = 38 THEN 38
  WHEN q.chapter_id = 39 THEN 39
  WHEN q.chapter_id = 40 THEN 40
END
FROM question q WHERE q.chapter_id BETWEEN 33 AND 40;