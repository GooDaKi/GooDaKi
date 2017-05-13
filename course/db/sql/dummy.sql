-- Course
INSERT INTO "Course" (name,description,created_at,updated_at,authorID,status) VALUES ('testcourse1','testcourse','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Course" (name,description,created_at,updated_at,authorID,status) VALUES ('testcourse2','testcourse','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Course" (name,description,created_at,updated_at,authorID,status) VALUES ('testcourse3','testcourse','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Course" (name,description,created_at,updated_at,authorID,status) VALUES ('testcourse4','testcourse','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Course" (name,description,created_at,updated_at,authorID,status) VALUES ('testcourse5','testcourse','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Course" (name,description,created_at,updated_at,authorID,status) VALUES ('testcourse6','testcourse','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);

-- Subject
INSERT INTO "Subject" (name,description,created_at,updated_at,authorID,status) VALUES ('testsubject1','testsubject','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Subject" (name,description,created_at,updated_at,authorID,status) VALUES ('testsubject2','testsubject','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Subject" (name,description,created_at,updated_at,authorID,status) VALUES ('testsubject3','testsubject','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Subject" (name,description,created_at,updated_at,authorID,status) VALUES ('testsubject4','testsubject','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Subject" (name,description,created_at,updated_at,authorID,status) VALUES ('testsubject5','testsubject','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Subject" (name,description,created_at,updated_at,authorID,status) VALUES ('testsubject6','testsubject','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "Subject" (name,description,created_at,updated_at,authorID,status) VALUES ('testsubject7','testsubject','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);

-- Career
INSERT INTO "CareerPath" (name,description,created_at,updated_at,authorID,status) VALUES ('testcareer1','testcareer','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "CareerPath" (name,description,created_at,updated_at,authorID,status) VALUES ('testcareer2','testcareer','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);
INSERT INTO "CareerPath" (name,description,created_at,updated_at,authorID,status) VALUES ('testcareer3','testcareer','2017-05-08 16:36:50.811000','2017-05-08 16:36:50.811000',1,1);


-- Subject in Course
INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (1,1,1);
INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (4,1,2);

INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (1,2,1);
INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (3,2,2);
INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (6,2,3);

INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (2,3,1);
INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (6,3,2);

INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (2,4,1);
INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (4,4,2);
INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (5,4,3);

INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (3,5,1);
INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering) VALUES (5,5,2);

-- Course in CareerPath
INSERT INTO "CourseInCareerPath" (courseID,careerID,ordering) VALUES (1,1,1);
INSERT INTO "CourseInCareerPath" (courseID,careerID,ordering) VALUES (3,1,2);

INSERT INTO "CourseInCareerPath" (courseID,careerID,ordering) VALUES (4,1,1);
INSERT INTO "CourseInCareerPath" (courseID,careerID,ordering) VALUES (2,2,2);
INSERT INTO "CourseInCareerPath" (courseID,careerID,ordering) VALUES (5,2,3);

INSERT INTO "CourseInCareerPath" (courseID,careerID,ordering) VALUES (1,3,1);