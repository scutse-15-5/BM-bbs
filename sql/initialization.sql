DROP DATABASE IF EXISTS bmbbs;
CREATE DATABASE bmbbs
  CHARACTER
  SET = utf8;
USE bmbbs;

CREATE TABLE account
(
  name      VARCHAR(16) NOT NULL,
  password  VARCHAR(16) NOT NULL,
  time      DATETIME    NOT NULL,
  signature TINYTEXT,
  icon      TINYTEXT NOT NULL ,
  PRIMARY KEY (name)
);

CREATE TABLE part
(
  partname VARCHAR(16),
  notice TEXT,
  PRIMARY KEY (partname)
);


CREATE TABLE topic
(
  id       VARCHAR(22),
  partname VARCHAR(16),
  time     DATETIME,
  name     VARCHAR(16),
  title    VARCHAR(30),
  content  TEXT,
  FOREIGN KEY (partname) REFERENCES part (partname)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (name) REFERENCES account (name)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  PRIMARY KEY (id)
);

CREATE TABLE comment
(
  topic_id VARCHAR(22),
  id       VARCHAR(22),
  time     DATETIME,
  name     VARCHAR(16),
  content  TEXT,
  FOREIGN KEY (topic_id) REFERENCES topic (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (name) REFERENCES account (name)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  PRIMARY KEY (id)
);