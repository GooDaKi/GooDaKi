CREATE TABLE IF NOT EXISTS "Subject" (
  subjectID   SERIAL,
  name        VARCHAR(255),
  description TEXT,
  created_at  TIMESTAMP,
  updated_at  TIMESTAMP,
  authorID    INT,
  status      BOOLEAN,
  PRIMARY KEY (subjectID)
);

CREATE TABLE IF NOT EXISTS "Course" (
  courseID    SERIAL,
  name        VARCHAR(255),
  description TEXT,
  created_at  TIMESTAMP,
  updated_at  TIMESTAMP,
  authorID    INT,
  status      BOOLEAN,
  PRIMARY KEY (courseID)
);

CREATE TABLE IF NOT EXISTS "CareerPath" (
  careerID    SERIAL,
  name        VARCHAR(255),
  description TEXT,
  created_at  TIMESTAMP,
  updated_at  TIMESTAMP,
  authorID    INT,
  status      BOOLEAN,
  PRIMARY KEY (careerID)
);

CREATE TABLE IF NOT EXISTS "ChunkInSubject" (
  chunkID   VARCHAR(50),
  subjectID INT,
  ordering  INT,
  PRIMARY KEY (chunkID, subjectID),
  FOREIGN KEY (subjectID) REFERENCES "Subject",
  UNIQUE (chunkID, subjectID, ordering)
);

CREATE TABLE IF NOT EXISTS "SubjectInCourse" (
  subjectID INT,
  courseID  INT,
  ordering     INT,
  PRIMARY KEY (subjectID, courseID),
  FOREIGN KEY (subjectID) REFERENCES "Subject" (subjectID),
  FOREIGN KEY (courseID) REFERENCES "Course" (courseID),
  UNIQUE (subjectID, courseID, ordering)
);

CREATE TABLE IF NOT EXISTS "CourseInCareerPath" (
  courseID INT,
  careerID INT,
  ordering    INT,
  PRIMARY KEY (courseID, careerID),
  FOREIGN KEY (courseID) REFERENCES "Course" (courseID),
  FOREIGN KEY (careerID) REFERENCES "CareerPath" (careerID),
  UNIQUE (courseID, careerID, ordering)
);

-- TODO: table for tags