create database if not exists askmate
;

create table if not exists question
(
	id serial not null
		constraint pk_question_id
			primary key,
	submission_time timestamp,
	view_number integer,
	vote_number integer,
	title text,
	message text,
	image text
)
;

create table if not exists answer
(
	id serial not null
		constraint pk_answer_id
			primary key,
	submission_time timestamp,
	vote_number integer,
	question_id integer
		constraint fk_question_id
			references question,
	message text,
	image text
)
;

create table if not exists comment
(
	id serial not null
		constraint pk_comment_id
			primary key,
	question_id integer
		constraint fk_question_id
			references question,
	answer_id integer
		constraint fk_answer_id
			references answer,
	message text,
	submission_time timestamp,
	edited_count integer
)
;

create table if not exists tag
(
	id serial not null
		constraint pk_tag_id
			primary key,
	name text
)
;

create table if not exists question_tag
(
	question_id integer not null
		constraint fk_question_id
			references question,
	tag_id integer not null
		constraint fk_tag_id
			references tag,
	constraint pk_question_tag_id
		primary key (question_id, tag_id)
)
;

create table if not exists users
(
	id serial not null
		constraint pk_user_id
			primary key
		constraint uc_users_id
			unique
		constraint users_id_key
			unique,
	username varchar(255)
		constraint uc_users_username
			unique,
	email varchar(255)
		constraint uc_users_email
			unique,
	password text,
	constraint uc_users
		unique (id, username, email)
)
;


ALTER TABLE question
  ADD column userid int;

ALTER TABLE question
ADD CONSTRAINT FK_userid FOREIGN KEY (userid) REFERENCES users(id);


ALTER TABLE answer
  ADD column userid int;

ALTER TABLE answer
ADD CONSTRAINT FK_userid FOREIGN KEY (userid) REFERENCES users(id);


ALTER TABLE comment
  ADD column userid int;

ALTER TABLE comment
ADD CONSTRAINT FK_userid FOREIGN KEY (userid) REFERENCES users(id);

