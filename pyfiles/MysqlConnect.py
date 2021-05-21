import pymysql
import traceback

class MysqlConnect:  # Connect to MySQL
    def __init__(self):
        pass

    def getConnect(self):
        '''
        db = pymysql.connect(
            host='39.108.63.191', user='root', passwd='Kswl2021', autocommit=True,
            port=3306, db='bilibili', charset='utf8'
        )
        '''
        db = pymysql.connect(
            host='39.108.63.191', user='root', passwd='Kswl2021', autocommit=True,
            port=3306, db='bilibili', charset='utf8'
        )
        
        return db

    def createTable1(self):
        # create the table PossibleTopUp
        table1 = '''CREATE TABLE `PossibleTopUp`
                        (
                            `ID` INT UNIQUE,
                            `Followings` INT, 
                            `Followers` BIGINT,
                            `Likes` BIGINT,
                            `Views` BIGINT,
                             PRIMARY KEY(ID)
                        )ENGINE=innodb DEFAULT CHARSET=utf8;'''
        db = self.getConnect()
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS `PossibleTopUp`;")
        cursor.execute(table1)
        cursor.close()
        db.close()

    '''
    def createTable2(self):
    # create the table for up's following
    table2 = CREATE TABLE `NewestTop100`
                    (
                        `ID` INT UNIQUE,
                        `Rank` INT,
                        `Followings` INT,
                         PRIMARY KEY(ID)
                    )ENGINE=innodb DEFAULT CHARSET=utf8;
    db = self.getConnect()
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `NewestTop100`;")
    cursor.execute(table2)
    cursor.close()
    db.close()
    '''

    def createTable2(self):
        # create the table for newest top 100
        table2 = '''CREATE TABLE `NewestTop100`
                        (   
                            `Rank` INT,
                            `ID` INT UNIQUE,
                            `Name` VARCHAR(50),
                            `Sex` VARCHAR(10),
                            `Birthday` VARCHAR(50),
                            `Place` VARCHAR(50),
                            `Level` INT,
                            `Face` VARCHAR(200),
                            `Followings` INT,
                            `Followers` BIGINT,
                            `Likes` BIGINT,
                            `Views` BIGINT,
                            `Sign` VARCHAR(200),
                            `Official` VARCHAR(200),
                             PRIMARY KEY(ID)
                        )ENGINE=innodb DEFAULT CHARSET=utf8;'''
        db = self.getConnect()
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS `NewestTop100`;")
        cursor.execute(table2)
        cursor.close()
        db.close()

    def insertInfo(self, sql):
        db = self.getConnect()
        cursor = db.cursor()
        try:
            cursor.execute(sql.encode('utf8'))
            db.commit()
            print("succeed...")
        except:
            print("failed...")
            db.rollback()
        finally:
            # Shutdown connect
            cursor.close()
            db.close()

    def getInsertToTable1Sql(self, tableName, ID, numFollowings, numFollowers, nunmLikes, numViews):
        sql = '''
            INSERT INTO `{}` VALUES ({}, {}, {}, {}, {});
            '''.format(tableName, ID, numFollowings, numFollowers, nunmLikes, numViews)
        return sql
    '''
    def getInsertToTable2Sql(self, tableName, ID, rank, numFollowings):
        sql = 
            INSERT INTO `{}` VALUES ({}, {}, {});
            .format(tableName, ID, rank, numFollowings)
        return sql
    '''

    def getInsertToTable2Sql(self, tableName, rank, id, name, sex, birthday, place, level, face, followings, followers, likes, views, sign, official):
        temp = [("'", r"\'"), ('"', r'\"')]
        for old, new in temp:
            name = name.replace(old, new)
            sign = sign.replace(old, new)
            official = official.replace(old, new)
        sql = '''
                INSERT INTO `{}` VALUES ({}, {}, '{}', '{}', '{}', '{}', {}, '{}', {}, {}, {}, {}, '{}', '{}');
              '''.format(tableName, rank, id, name, sex, birthday, place, level, face, followings, followers, likes, views, sign, official)
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
            cursor.close()
            db.close()
        return result