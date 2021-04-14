import pymysql
import traceback

class MysqlConnect:  # Connect to MySQL
    def __init__(self):
        pass

    def getConnect(self):
        db = pymysql.connect(
            host='localhost', user='root', passwd='TSxsy240319!',
            port=3306, db='birank', charset='utf8'
        )
        return db

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


    def queryOutCome(self, sql):
        # Establish connect
        db = self.getConnect()
        # set up a cursor
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
        except:
            traceback.print_exc()
            db.rollback()
        finally:
            # Shutdown connect
            db.close()
        return result

    def getCreateTableSql(self, tableName):
        sql = '''CREATE TABLE `{}` 
        (
            `rank` INT,
            `title` VARCHAR(60),
            `videoID` VARCHAR(40), 
            `score` INT,
            `play` VARCHAR(40),
            `view` VARCHAR(40),
            `upName` VARCHAR(40),
            `upID` INT,
             PRIMARY KEY(videoID)
        )ENGINE=innodb DEFAULT CHARSET=utf8;'''.format(tableName)
        return sql

    def getInsertToTableSql(self, tableName, rank, title, videoID, score, play, view, upName, upID):
        sql = '''
        INSERT INTO `{}` VALUES ('{}','{}','{}','{}','{}','{}','{}','{}');
        '''.format(tableName, rank, title, videoID, score, play, view, upName, upID)
        return sql

    def createTable(self, tableName, sql):
        db = self.getConnect()
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS `{}`".format(tableName))
        cursor.execute(sql)
        db.close()