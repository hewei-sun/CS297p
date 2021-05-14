from pyfiles.MysqlConnect import MysqlConnect
from pyfiles.Uploader import Uploader

def webUpRank():
    mysqlconnect = MysqlConnect()
    sql = "SELECT `ID`,`Followings`,`Rank` from `NewestTop100` ORDER BY `Rank`;"
    upList = [(ID, Followings, Rank) for (ID, Followings, Rank,) in mysqlconnect.queryOutCome(sql)]
    for up, _, _ in upList:
        UP = Uploader(up)
        UP.crawl_basic()
        print(UP.__dict__)
    return upList

if __name__ == "__main__":
    webUpRank()