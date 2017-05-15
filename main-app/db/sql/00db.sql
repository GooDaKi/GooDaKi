-- progress bigint means that what sub-element the user complete
-- means that course cannot have more than 64 subjects,
-- subjects cannot have more than 64 chunks, etc.

create table "User" (
    userID      serial,
    username    varchar(64),
    displayname varchar(64),
    password    varchar(255),
    email       varchar(255),
    firstname   varchar(255),
    lastname    varchar(255),
    primary key (userID),
    unique (username),
    unique (email),
    unique (displayname)
);

create table "Take_Chunk" (
    userID    int,
    chunkID   varchar(64),
    score     int, -- if this chunk is a test
    type      int, -- 1 is test, 0 otherwise TODO reconsider type
    completed date,
    primary key (userID, chunkID),
    foreign key (userID) references "User" (userID)
);

create table "Take_Course" (
    userID    int,
    courseID  int,
    progress  bigint,
    started   date,
    completed date,
    updated   date,
    primary key (userID, courseID),
    foreign key (userID) references "User" (userID)
);

create table "Take_Subject" (
    userID    int,
    subjectID int,
    progress  bigint,
    started   date,
    completed date,
    updated   date,
    primary key (userID, subjectID),
    foreign key (userID) references "User" (userID)
);

create table "Take_Career" (
    userID    int,
    careerID  int,
    progress  bigint,
    started   date,
    completed date,
    updated   date,
    primary key (userID, careerID),
    foreign key (userID) references "User" (userID)
);
