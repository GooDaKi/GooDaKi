CREATE TYPE sex_enum AS ENUM ('M', 'F');
CREATE TABLE IF NOT EXISTS "User" (
    userID      SERIAL,
    username    VARCHAR(64),
    password    VARCHAR(255),
    email       VARCHAR(255),
    firstname   VARCHAR(255),
    lastname    VARCHAR(255),
    sex         sex_enum,
    phone       VARCHAR(15),
    birthdate   DATE,
    address     TEXT,
    PRIMARY KEY (userID),
    UNIQUE (username),
    UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS "Portfolio" (
    portID      SERIAL,
    education   TEXT,
    PRIMARY KEY (portID)
);

CREATE TABLE IF NOT EXISTS "Has_portfolio" (
    userID      INT,
    portID      INT,
    PRIMARY KEY (userID, portID),
    FOREIGN KEY (userID)  REFERENCES "User" (userID),
    FOREIGN KEY (portID) REFERENCES "Portfolio" (portID)
);

CREATE TABLE IF NOT EXISTS "Taking_course" (
    portID      INT,
    courseID    INT UNIQUE,
    subjectID  	INT,
    chunkID 	INT,
    PRIMARY KEY (portID, courseID),
    FOREIGN KEY (portID) REFERENCES "Portfolio" (portID)
);


CREATE TABLE IF NOT EXISTS "Taken_course" (
    portID      INT,
    courseID    INT,
    subjectID	INT,
    chunkID		INT,
	score 		REAL,
    PRIMARY KEY (portID,courseID,subjectID,chunkID),
    FOREIGN KEY (portID) REFERENCES "Portfolio" (portID)
);


CREATE TABLE IF NOT EXISTS "Taking_course_score" (
	portID		INT,
	courseID	INT,
	subjectID	INT,
	chunkID		INT,
	score 		REAL,
	PRIMARY KEY (portID,courseID,subjectID,chunkID),
	FOREIGN KEY (portID) REFERENCES "Portfolio" (portID),
	FOREIGN KEY (courseID) REFERENCES "Taking_course" (courseID)

);