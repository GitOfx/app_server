import sqlite3
import sys

#sqlite3.connect(dbName) will create the db if not exists
# http://www.pythondoc.com/flask-sqlalchemy/index.html

dbName = "app_service.db"


class BaseTable:
    def __init__(self,table_name):
        self.table_name = table_name
        pass
    
    def create_table(self,**field_kw):
        sql = "create %s if not exists " % self.table_name

class Table_user:
    table_name = 'user_table'
    def __init__(self):
        self.create_table()
 
    def insert_user(self,user_name,password):
        sql = 'insert into %s(username,password) values (?,?)' % self.table_name
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        cursor.execute(sql,(user_name,password))
        print(sql+" %s %s "% (user_name,password))
        result = cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()
        if result > 0:
            return True
        else:
            return False

    def create_table(self):
        sql = "create table if not exists  %s(id integer primary key autoincrement,username  string not null, password string not null)"% self.table_name
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        cursor.execute(sql)
        print(sql)
        cursor.close()
        conn.commit()
        conn.close()

    def select_user(self,username,password): 
        sql = "select * from %s where username = ? and password = ?" %self.table_name
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        cursor.execute(sql, (username,password)) 
        print(sql+(" %s %s "% (username,password)))
        result = cursor.fetchall()
        print(result)
        cursor.close()
        conn.commit()
        conn.close()
        return result

    def selectAll(self):
        sql = "select * from %s " %self.table_name
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        cursor.execute(sql) 
        print(sql)
        result = cursor.fetchall()
        print(result)
        cursor.close()
        conn.commit()
        conn.close()
        return self.resultToUserList(result)

    def resultToUserList(self,result):
        user_list = []
        for usertuple in result:
            user = Table_user()
            user.id = usertuple[0]
            user.username = usertuple[1]
            user.password = usertuple[2]
            user_list.append(user)
        return user_list
    
    def __repr__(self):
        return "id: %s name: %s password: %s" % (self.id,self.username,self.password)

    @staticmethod
    def selectAllNews():

        pass
#命令行

if __name__ == '__main__':
    user = Table_user()
    user.select_user('ofx','password') 