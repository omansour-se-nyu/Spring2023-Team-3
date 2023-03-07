import psycopg2
from pandas import DataFrame

class PostgresHandler():
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.cur = None
        #self.con = self.connect()


    def connect(self):
        try:
            self.con = psycopg2.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.database
            )
            print(self.con)
            self.cur = self.con.cursor()
        except Exception as error:
            print(error)

    def getData(self, tableName):
        try:
            #if self.con == None:
            self.con = self.connect()
            sql = "select * from " + str(tableName)
            self.cur.execute(sql)
            df = DataFrame(self.cur.fetchall())
            print(df)
            return df
        except Exception as error:
            print(error)
        finally:
            if self.con is not None:
                self.con.close()
            if self.cur is not None:
                self.cur.close()

    def getQuery(self, query):

        try:
            #if self.con == None:
            self.connect()
            sql = query
            self.cur.execute(sql)
            df = DataFrame(self.cur.fetchall())

        try:
            self.connect()
            sql = query
            self.cur.execute(sql)

            df = DataFrame(self.cur.fetchall(),columns=['UserName', 'Password'])

            print(df)
            return df
        except Exception as error:
            print(error)
        finally:
            if self.con is not None:
                self.con.close()
            if self.cur is not None:
                self.cur.close()

    def insertData(self, query):
        try:
            self.connect()
            # sql = "insert into " + tableName + " (" + schema  + ") values (" + data + ")"
            sql = query
            self.cur.execute(sql)

            self.con.commit()
        except Exception as error:
            print(error)
            return error
        finally:
            if self.con is not None:
                self.con.close()
            if self.cur is not None:
                self.cur.close()

        if self.con == None:
            try:
                self.con = self.connect()
                sql = query
                self.cur.execute(sql)
                df = DataFrame(self.cur.fetchall())
                print(df)
                return df
            except Exception as error:
                print(error)
            finally:
                if self.con is not None:
                    self.con.close()
                if self.cur is not None:
                    self.cur.close()

    def insertData(self, query):
        try:
            #if self.con == None:
            self.connect()
            # sql = "insert into " + tableName + " (" + schema  + ") values (" + data + ")"
            sql = query
            self.cur.execute(sql)
            if self.con == None:
                self.con = self.connect()
            self.con.commit()
        except Exception as error:
            print(error)
        finally:
            if self.con is not None:
                self.con.close()
            if self.cur is not None:
                self.cur.close()


    def createTable(self, tableName, schema, prefix=None):
        try:
            #if self.con == None:
            self.connect()
            print(self.con)
            if prefix:
                self.cur.execute(prefix)
                self.con.commit()
            sql = "create table if not exists " + str(tableName) + " ( " + str(schema) + " ) "
            self.cur.execute(sql)
            self.con.commit()
        except Exception as error:
            print(error)
        finally:
            if self.con is not None:
                self.con.close()
                print('aidughaiu', self.con)
            if self.cur is not None:
                self.cur.close()

    def createTable(self, tableName, schema):
        if self.con == None:
            try:
                self.con = self.connect()
                sql = "create table if not exists " + str(tableName) + " ( " + str(schema)
                self.cur.execute(sql)
                self.con.commit()
            except Exception as error:
                print(error)
            finally:
                if self.con is not None:
                    self.con.close()
                if self.cur is not None:

                    self.cur.close()

    def exists(self,sql):
        try:
            self.connect()
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as error:
            print(error)
            return error
        finally:
            if self.con is not None:
                self.con.close()
            if self.cur is not None:
                self.cur.close()
                    self.cur.close()


