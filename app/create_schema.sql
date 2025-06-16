drop database if exists CP_test_db;

create database CP_test_db;

use CP_test_db;

create table users (
    user_UUID varchar(37) primary key,
    user_name varchar(45) not null unique,
    user_email varchar(60) not null unique,
    user_pass_hash varchar(256) not null 
) engine innodb;

create table notes (
    note_UUID varchar(37) primary key,
    note_name varchar(512) not null,
    note_text mediumtext,
    user_UUID varchar(37) not null,
    foreign key (user_UUID) references users(user_UUID)
) engine innodb;

create table note_files (
    file_UUID_name varchar(37) primary key,
    file_name varchar(512) not null,
    -- file_path varchar(512) not null,
    note_UUID varchar(37) not null,
    foreign key (note_UUID) references notes(note_UUID)
) engine innodb;

