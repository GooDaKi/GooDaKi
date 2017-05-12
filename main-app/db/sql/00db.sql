create table "User" (
    userID      serial,
    username    varchar(64),
    displayname varchar(64),
    password    varchar(255),
    email       varchar(255),
    firstname   varchar(255),
    lastname    varchar(255),
    primary key (userID),
    unique (email),
    unique (username),
    unique (displayname)
);

