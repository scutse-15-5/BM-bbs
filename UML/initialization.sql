drop database if exists bmbbs;
create database bmbbs;
use bmbbs;

create table account(
name varchar(8),
password varchar(16)not null,
primary key (name));

create table part(
partname varchar(8),
primary key (partname));

create table topic(
partname varchar(8),
ownername varchar(8),
id varchar(11),
content varchar(50),
foreign key (partname) references part(partname) on delete cascade on update cascade,
foreign key (ownername) references account(name) on delete cascade on update cascade,
primary key (id,partname,ownername));

create table notice(
partname varchar(8),
content varchar(50),
foreign key (partname) references part(partname) on delete cascade on update cascade,
primary key (partname,content));

create table comment(
topicid varchar(8),
ownername varchar(8),
layer varchar(4),
content varchar(50), 
foreign key (topicid) references topic(id) on delete cascade on update cascade,
foreign key (ownername) references account(name) on delete cascade on update cascade,
primary key (topicid,ownername,layer));

#帖子id是发布时间