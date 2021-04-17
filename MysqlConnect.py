import pymysql
import traceback

class MysqlConnect:  # Connect to MySQL
    def __init__(self):
        pass

    def getConnect(self):
        db = pymysql.connect(
            host='localhost', user='root', passwd='TSxsy240319!', autocommit=True,
            port=3306, db='BilibiliUp', charset='utf8'
        )
        return db

    def createTable1(self):
        # create the table PossibleTopUp
        table1 = '''CREATE TABLE `PossibleTopUp`
                        (
                            `ID` VARCHAR(40) UNIQUE,
                            `Followings` VARCHAR(40), 
                            `Followers` VARCHAR(40),
                            `Likes` VARCHAR(40),
                            `Views` VARCHAR(40),
                             PRIMARY KEY(ID)
                        )ENGINE=innodb DEFAULT CHARSET=utf8;'''
        db = self.getConnect()
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS `PossibleTopUp`;")
        cursor.execute(table1)
        db.close()

    def createTable2(self):
        # create the table for up's following
        table2 = '''CREATE TABLE `NewestTop100`
                        (
                            `ID` VARCHAR(40) UNIQUE,
                             PRIMARY KEY(ID)
                        )ENGINE=innodb DEFAULT CHARSET=utf8;'''
        db = self.getConnect()
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS `NewestTop100`;")
        cursor.execute(table2)
        db.close()

    def insertInfo(self, sql):
        db = self.getConnect()
        cursor = db.cursor()
        try:
            cursor.execute(sql.encode('utf8'))
            db.commit()
            print("sucessed...")
        except:
            print("failed...")
            db.rollback()

    def getInsertToTable1Sql(self, tableName, ID, numFollowings, numFollowers, nunmLikes, numViews):
        sql = '''
            INSERT INTO `{}` VALUES ('{}','{}','{}','{}','{}');
            '''.format(tableName, ID, numFollowings, numFollowers, nunmLikes, numViews)
        return sql

    def getInsertToTable2Sql(self, tableName, ID):
        sql = '''
            INSERT INTO `{}` VALUES ('{}');
            '''.format(tableName, ID)
        return sql

    def queryOutCome(self, sql):
        # Establish connect
        db = self.getConnect()
        # set up a cursor
        cursor = db.cursor()
        result=None
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except:
            traceback.print_exc()
            db.rollback()
        finally:
            # Shutdown connect
            db.close()
        return result