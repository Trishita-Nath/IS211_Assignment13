DROP TABLE IF EXISTS students;

CREATE TABLE students (
id INTEGER PRIMARY KEY NOT NULL,
first_name TEXT,
last_name TEXT
);

DROP TABLE IF EXISTS quizzes;

CREATE TABLE quizzes (
id INTEGER PRIMARY KEY NOT NULL,
subject TEXT,
question_count INTEGER,
quiz_date DATE 
);

DROP TABLE IF EXISTS results;

CREATE TABLE results (
student_id INTEGER NOT NULL,
quiz_id INTEGER NOT NULL,
quiz_score INTEGER
);

INSERT INTO students (id, first_name, last_name) VALUES (1000, 'John', 'Smith');
INSERT INTO quizzes (id, subject ,question_count, quiz_date) VALUES (100, 'Python Basics', '5', 'February, 5th, 2015');
INSERT INTO results (student_id, quiz_id, quiz_score) VALUES (1000, 100, 85);