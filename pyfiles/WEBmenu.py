from pyfiles.MysqlConnect import MysqlConnect

def upMe():
    mysqlconnect = MysqlConnect()
    sql = "SELECT `ID` AS id,`Name` AS name FROM `NewestTop100`"
    upList = [(id,name) for (id,name,) in mysqlconnect.queryOutCome(sql)]
    return upList

def viMe():
    mysqlconnect = MysqlConnect()
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES'
    field = [tb for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:4] == 'RANK']
    vlist = []
    for f in field:
        sql = f"SELECT `BVid`,`Title` from `{f}` ORDER BY `Rank`;"
        vli = [(BVid,Title) for (BVid,Title,) in mysqlconnect.queryOutCome(sql)]
        vlist.append(vli)
    return vlist