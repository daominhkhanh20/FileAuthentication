CREATE database AuthenticationFile;
USE AuthenticationFile;
CREATE TABLE InformationFile(
file_name varchar(30) primary key,
file_path varchar(200),
h_0 varchar(300)
);

/*
Alter table InformationFile add column h_0 varchar(300);
insert into InformationFile(file_name,file_path) values('cc.txt','/home/daominhkhanh/Documents');

update InformationFile Set h_0="kk" where file_name='kk.txt';
DELETE FROM InformationFile where file_name='birthday_concat.mp4';
*/