from postgres_connect import PostgresHandler

schema_login= "username varchar(30) unique not null, password varchar(30) not null"

# table: patient \
#             -> id: varchar
#             -> name: varchar
#             -> gender: enumerate
#             -> age: int
#             -> ssn: varchar
#             -> phone: varchar
#             -> email: varchar
#             -> address: varchar
prefix_patients="create type gen as enum('Male', 'Female', 'Other')"
schema_patients="id varchar(8) unique not null, name varchar(30), gender gen, age smallint not null, ssn varchar(9) unique not null, phone varchar(10), email varchar(30), address varchar(200)"

# table: records \
#             -> id: varchar
#             -> record_id: varchar
#             -> last_modified: timestamp
#             -> content: text
schema_records="id varchar(8) unique not null, record_id varchar(8) unique not null, last_modified timestamp, content text"

DB = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
#DB.createTable('login', schema_login)
DB.createTable('patients', schema_patients, prefix_patients)
#DB.createTable('records', schema_records)

# new table test
id='\'11111111\''
record_id='\'22222222\''
content='\'Dummy patient record.\''
name='\'Jacky Chen\''
gender='\'Male\''
age='\'42\''
ssn='\'123456789\''
phone='\'3333333333\''
email='\'jack@example.com\''
address='\'805 Stanley St, Brooklyn, New York\''
#DB.insertData('insert into records(id, record_id, content) values( '+id+', '+record_id+', '+content+')')
#DB.insertData('insert into patients(id, name, gender, age, ssn, phone, email, address) values('+id+', '+name+', '+gender+', '+age+', '+ssn+', '+phone+', '+email+', '+address+')')
df1=DB.getQuery('select * from records')
print(df1.at[0, 1])
df2=DB.getQuery('select * from patients')
print(df2.at[0, 1])