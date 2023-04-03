create table login (
id varchar(8) primary key 
username varchar(32) not null
password varchar(32) not null
);

create table patients (
id varchar(8) primary key
name varchar(30) not null
gender gen not null
ssn varchar(9) unique not null
phone varchar(10)
email varchar(30)
address varchar(200)
);

create table records (
patient_id varchar(8) 
doctor_id varchar(8)
record_id varchar(8) primary key
last_modified timestamp
content text not null
foreign key (patient_id) references patients(id)
foreign key (doctor_id) references login(id)
);