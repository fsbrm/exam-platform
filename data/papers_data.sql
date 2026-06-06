USE exam_platform;

-- Clear existing papers
DELETE FROM paper_question;
DELETE FROM exam_paper;
ALTER TABLE exam_paper AUTO_INCREMENT = 1;

-- Insert exam papers (2009-2021)
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (1, 1, 2009, '2009年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (2, 1, 2010, '2010年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (3, 1, 2011, '2011年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (4, 1, 2012, '2012年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (5, 1, 2013, '2013年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (6, 1, 2014, '2014年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (7, 1, 2015, '2015年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (8, 1, 2016, '2016年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (9, 1, 2017, '2017年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (10, 1, 2018, '2018年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (11, 1, 2019, '2019年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (12, 1, 2020, '2020年408计算机基础综合真题', 150, 180, 47);
INSERT INTO exam_paper (id, subject_id, year, name, total_score, duration, question_count) VALUES (13, 1, 2021, '2021年408计算机基础综合真题', 150, 180, 47);

-- Link questions to papers based on year
INSERT INTO paper_question (paper_id, question_id, sort_order)
SELECT ep.id, q.id, q.id - (SELECT MIN(id) FROM question WHERE year = ep.year) + 1
FROM exam_paper ep
JOIN question q ON q.year = ep.year
ORDER BY ep.year, q.id;