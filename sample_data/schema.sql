create database askmate;

create table if not exists question
(
  id              serial not null
    constraint pk_question_id
    primary key,
  submission_time timestamp,
  view_number     integer,
  vote_number     integer,
  title           text,
  message         text,
  image           text
);

create table if not exists answer
(
  id              serial not null
    constraint pk_answer_id
    primary key,
  submission_time timestamp,
  vote_number     integer,
  question_id     integer
    constraint fk_question_id
    references question,
  message         text,
  image           text
);

create table if not exists comment
(
  id              serial not null
    constraint pk_comment_id
    primary key,
  question_id     integer
    constraint fk_question_id
    references question,
  answer_id       integer
    constraint fk_answer_id
    references answer,
  message         text,
  submission_time timestamp,
  edited_count    integer
);

create table if not exists tag
(
  id   serial not null
    constraint pk_tag_id
    primary key,
  name text
);

create table if not exists question_tag
(
  question_id integer not null
    constraint fk_question_id
    references question,
  tag_id      integer not null
    constraint fk_tag_id
    references tag,
  constraint pk_question_tag_id
  primary key (question_id, tag_id)
);


