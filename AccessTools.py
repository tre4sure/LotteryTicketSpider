import pymysql.cursors
import json
from ticketObj import ticketInfo

class AccessTools:

    def __init__(self):
        # self.host = host
        # self.username = userName
        # self.password = passWord
        return

    def initMySql(self, host, userName, passWord):
        self.host = host
        self.username = userName
        self.password = passWord
    
    def ReadFromMySql(self):

        return

    def ReadFromText(self):
        
        return

    def WriteToMySql(self, dbName, sql):
        connection = pymysql.connect(host = self.host,
                        user = self.username,
                        password = self.password,
                        db = dbName,
                        charset = 'utf8',
                        cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.commit()
        return

    def WriteToText(self, data):
        json_str = json.dumps(data)
        print(json_str)
        with open('C:\\Users\\Dioooooooor\\Desktop\\data.json', 'w') as json_file:
            json_file.write(json_str)
        return