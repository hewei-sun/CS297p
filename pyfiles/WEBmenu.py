from pyfiles.MysqlConnect import MysqlConnect

def upMe():
    mysqlconnect = MysqlConnect()
    sql = "SELECT `ID` AS id,`Name` AS name FROM `NewestTop100`"
    upList = [(id,name) for (id,name,) in mysqlconnect.queryOutCome(sql)]
    return upList