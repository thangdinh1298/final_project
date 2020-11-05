DROP DATABASE IF EXISTS CourseManager;
CREATE DATABASE IF NOT EXISTS CourseManager;
USE CourseManager;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS StudyMaterial;
DROP TABLE IF EXISTS Homework;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS User_Course;

CREATE TABLE IF NOT EXISTS Course (
	course_id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100),
	year INT,
	semester INT,
	description VARCHAR(500),
	course_length INT,
	PRIMARY KEY(course_id)
);

CREATE TABLE IF NOT EXISTS StudyMaterial (
	study_material_id INT NOT NULL AUTO_INCREMENT,
	course_id INT NOT NULL,
	week INT NOT NULL,
	PRIMARY KEY(study_material_id),
	FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

CREATE TABLE IF NOT EXISTS Homework (
	homework_id INT NOT NULL AUTO_INCREMENT,
	course_id INT NOT NULL,
	week INT NOT NULL,
	PRIMARY KEY(homework_id),
	FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

CREATE TABLE IF NOT EXISTS User (
	user_id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100),
	username VARCHAR(100),
	password VARCHAR(100),
	email VARCHAR(100),
	phone VARCHAR(15),
	PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS User_Course (
	id INT NOT NULL AUTO_INCREMENT,
	course_id INT NOT NULL,
	user_id INT NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY (course_id) REFERENCES Course(course_id),
	FOREIGN KEY (user_id) REFERENCES User(user_id)
);
