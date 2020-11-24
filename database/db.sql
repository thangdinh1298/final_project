DROP DATABASE IF EXISTS CourseManager;
CREATE DATABASE IF NOT EXISTS CourseManager;
USE CourseManager;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS CourseSchedule;
DROP TABLE IF EXISTS StudyMaterial;
DROP TABLE IF EXISTS Homework;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UserCourse;
DROP TABLE IF EXISTS Announcement;
DROP TABLE IF EXISTS Role;
DROP TABLE IF EXISTS UserRole;

CREATE TABLE IF NOT EXISTS User (
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(100) UNIQUE,
	password VARCHAR(100),
	email VARCHAR(100),
	phone VARCHAR(15),
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Course (
   id INT NOT NULL AUTO_INCREMENT,
   name VARCHAR(100),
   start_date DATE,
   end_date DATE,
   description MEDIUMTEXT,
   info MEDIUMTEXT,
   course_length INT,
   user_id INT NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CourseSchedule (
   id INT NOT NULL AUTO_INCREMENT,
   course_id INT NOT NULL,
   day_of_week INT,
   minute_of_day INT,
   PRIMARY KEY(id),
   FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE
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

-- FIXME: This table design is very bad but sql alchemy wont reflect this table if we remove id
-- and make primary key a composite key of course_id and user_id
CREATE TABLE IF NOT EXISTS UserCourse (
   id INT NOT NULL AUTO_INCREMENT,
	course_id INT NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY (course_id) REFERENCES Course(id),
	FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Role (
   id INT NOT NULL AUTO_INCREMENT,
   role VARCHAR(50),
   PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS UserRole (
   user_id INT NOT NULL,
   role_id INT NOT NULL,
   PRIMARY KEY (user_id, role_id),
   FOREIGN KEY (user_id) REFERENCES User(id),
   FOREIGN KEY (role_id) REFERENCES Role(id)
);
