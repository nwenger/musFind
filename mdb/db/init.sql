create database mdb;

use mdb;

create table test (id smallint unsigned not null auto_increment, string varchar(64), constraint id primary key (id));
insert into test (id, string) values (1, 'hello');
insert into test (id, string) values (2, 'world');
insert into test (id, string) values (3, '!');
commit;
