DROP DATABASE IF EXISTS CourseManager;
CREATE DATABASE IF NOT EXISTS CourseManager;
USE CourseManager;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS StudyMaterial;
DROP TABLE IF EXISTS Homework;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS User_Course;
DROP TABLE IF EXISTS Announcement;

CREATE TABLE IF NOT EXISTS Course (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100),
	year INT,
	semester INT,
	description MEDIUMTEXT,
   info MEDIUMTEXT,
	course_length INT,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS StudyMaterial (
	course_id INT NOT NULL,
	week INT NOT NULL,
	description MEDIUMTEXT,
	PRIMARY KEY(course_id, week),
	FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE IF NOT EXISTS Homework (
	course_id INT NOT NULL,
	week INT NOT NULL,
	description MEDIUMTEXT,
	PRIMARY KEY(course_id, week),
	FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE IF NOT EXISTS Announcement (
   id INT NOT NULL AUTO_INCREMENT,
   description MEDIUMTEXT,
   course_id INT NOT NULL,
   created_date DATETIME,
   PRIMARY KEY(id),
   FOREIGN KEY (course_id) REFERENCES Course(id)
);

CREATE TABLE IF NOT EXISTS User (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100),
	username VARCHAR(100),
	password VARCHAR(100),
	email VARCHAR(100),
	phone VARCHAR(15),
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS User_Course (
	id INT NOT NULL AUTO_INCREMENT,
	course_id INT NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY (course_id) REFERENCES Course(id),
	FOREIGN KEY (user_id) REFERENCES User(id)
);
