import psycopg2
from pandas import DataFrame
from postgres_connect import PostgresHandler
import os

class PostgresToolBox():
    def __init__(self, dbname='postgres', user='postgres', pwd='', host='localhost', port='5432', remotedb=None):
        self.dbname=dbname
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
        if not remotedb:
            self.remotedb=PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.pwd,
            host=self.host,
            port=self.port
        )
        self.cur=self.conn.cursor()

    def deconnect(self):
        self.cur.close()
        self.conn.close()
        self.conn, self.cur=None, None


    def exists(self,sql):
        try:
            self.connect()
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as error:
            print(error)
            return error
    def getRow(self, query):
        try:
            self.connect()
            sql = query
            self.cur.execute(sql)

            df = self.cur.fetchone()
            print(df)
            return df
        except Exception as error:
            print(error)

    def getRowAll(self, query, cols):
        try:
            self.connect()
            sql = query
            self.cur.execute(sql)

            df = DataFrame(self.cur.fetchall(), columns = cols)
            print(df)
            return df
        except Exception as error:
            print(error)
    
    def executeSql(self, sql):
        # local database has higher priority
        # do local changes anyway
        try:
            self.connect()
            self.cur.execute(sql)
            self.conn.commit()
            print("execute local command:", sql)
            path=os.path.dirname(os.path.abspath(__file__)) + "/../files/operations.txt"
            # has access to remote db
            if self.remotedb.connect():
                # first see if legacy operations exist
                if os.path.getsize(path) > 0:
                    with open(path, mode='r') as file:
                        for line in file:
                            # SUBJECT TO CHANGE !!!
                            if line.strip()=='':
                                continue
                            self.remotedb.cur.execute(line.replace("public","mentcare"))
                            self.remotedb.con.commit()
                            print("execute legacy command:", line)
                # reset operation file
                with open(path, mode='w') as file:
                    file.write('')
                self.remotedb.cur.execute(sql.replace("public","mentcare"))
                self.remotedb.con.commit()
                print("execute remote command", sql)
            # no remote access
            else:
                # no remote connection, only do local changes and stack operations in files
                with open(path, mode='a') as file:
                    file.write('\n'+sql)
                    print("add command as a legacy command:", sql)
        except Exception as error:
            print(error)
            return error
        #return df

