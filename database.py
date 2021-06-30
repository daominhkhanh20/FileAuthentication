from codecs import decode
from mysql import connector 
from mysql.connector import Error
import os 
from base64 import b64encode,decodebytes

class Database:
    def __init__(self):
        try:
            # --------------MYSQL--------------------------
            self.connection=connector.connect(host='localhost',
                                        database='AuthenticationFile',
                                        user='daominhkhanh',
                                        password='daominhkhanh@'
                            )
        except Error as e:
            print("Error while connecting to MYSQL",e)
        
        self.my_cursor=self.connection.cursor()
    
    def insert_file(self,file_name,file_path,h0):
        try:
            h0=b64encode(h0).decode('utf-8')
            self.my_cursor.execute("insert into InformationFile(file_name,file_path,h_0) values('{}','{}','{}');".format(file_name,file_path,h0))
            self.connection.commit()
            print("Insert success")
        except Error as e:
            print(e)

    def insert_h0(self,h0,file_name):
        try:
            h0=b64encode(h0).decode('utf-8')
            self.my_cursor.execute("UPDATE InformationFile SET h_0='{}' WHERE file_name='{}'".format(h0,file_name))
            self.connection.commit()
        except Error as e:
            print(e)
    
    def get_path(self,file_name):
        try:
            self.my_cursor.execute("Select file_path from AuthenticationFile.InformationFile where file_name='{}'".format(file_name))
            my_result=self.my_cursor.fetchall()
            if len(my_result)>2:
                print("error")
                return None
            return my_result[0][0]
        except Error as e:
            print(e)

    def get_h0(self,file_name):
        try:
            self.my_cursor.execute("SELECT h_0 from AuthenticationFile.InformationFile where file_name='{}'".format(file_name))
            result=self.my_cursor.fetchall()
            if len(result)>2:
                return None
            result=result[0][0]
            result=decodebytes(result.encode('utf-8'))
            return result
        except Error as e:
            print(e)

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Closed success")

# db=Database()
# temp=os.urandom(10)
# print(temp)
# db.insert_h0(os.urandom(10),'cc.txt')
# print(db.get_h0('123.txt'))