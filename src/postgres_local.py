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
        self.conn, self.cur=self.connect()

    def connect(self):
        conn, cur=None, None        
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.pwd,
            host=self.host,
            port=self.port
        )
        cur=conn.cursor()    
        return conn, cur
    
    def deconnect(self):
        self.cur.close()
        self.conn.close()
        self.conn, self.conn=None, None
    
    def executeSql(self, sql, ifRemote=True):
        # local database has higher priority
        # do local changes anyway
        sql=sql.strip()
        self.cur.execute(sql)
        self.conn.commit()
        print("execute local command:", sql)
        df=None
        if "select" in sql.lower():
            df=DataFrame(self.cur.fetchall())
        
        if ifRemote:
            path=os.path.dirname(os.path.abspath(__file__)) + "/../files/operations.txt"
            # has access to remote db
            if self.remotedb.connect():
                # first see if legacy operations exist
                if os.path.getsize(path) > 0:
                    with open(path, mode='r') as file:
                        for line in file:
                            # SUBJECT TO CHANGE !!!
                            self.remotedb.cur.execute(line.strip())
                            self.remotedb.con.commit()
                            print("execute legacy command:", line)
                # reset operation file
                with open(path, mode='w') as file:
                    file.write('')
                # execute current command to remote
                self.remotedb.cur.execute(sql)
                self.remotedb.con.commit()
                print("execute remote command", sql)
            # no remote access
            else:
                # no remote connection, only do local changes and stack operations in files
                with open(path, mode='a') as file:
                    file.write('\n'+sql)
                    print("add command as a legacy command:", sql)
        
        return None if df is None or df.empty else df

