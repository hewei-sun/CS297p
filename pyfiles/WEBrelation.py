from pyfiles.MysqlConnect import MysqlConnect

def checkName(id):
    mysqlconnect=MysqlConnect()
    sql = f"SELECT `Name` FROM `NewestTop100` WHERE `ID` = {id}"
    name = [name for (name,) in mysqlconnect.queryOutCome(sql)][0]
    return name

def showRelation():
    mysqlconnect = MysqlConnect()
    #sql = 'SELECT `ID` FROM `PossibleTopUp'
    sql = 'SELECT `ID` FROM `NewestTop100`'
    ups = [id for(id,)in mysqlconnect.queryOutCome(sql)]
    relation = []
    up = []
    uploader = set()
    for u in ups:
        #sql=f"SELECT * FROM `following{up}` WHERE EXISTS(SELECT * FROM `PossibleTopUp` WHERE `ID`=`following{up}`.`ID`)"
        sql=f"SELECT f.`ID`,n.`Name` FROM (SELECT * FROM `following{u}` WHERE EXISTS(SELECT * FROM `NewestTop100` WHERE `ID`=`following{u}`.`ID`)) f JOIN (SELECT * FROM `NewestTop100`) n ON f.`ID` = n.`ID`"
        following=[(id,name) for(id,name,)in mysqlconnect.queryOutCome(sql)]
        if len(following) == 0:
            continue
        name = checkName(u)
        if not u in uploader:
            up.append([u,name])
            uploader.add(u)
        for f in following:
            relation.append([f[1],name])
            if not f[0] in uploader:
                up.append([f[0],f[1]])
                uploader.add(f[0])
    return relation,up