from pyfiles.WEBuploader import Uploader
from pyfiles.WEBsingleQueries import ifPossible
from pyfiles.MysqlConnect import MysqlConnect

def uploaderAna(id):
    isPoss = ifPossible(id)
    up = Uploader(id,isPoss)
    up.crawl_basic()
    #up.crawl_videoList()
    ups = []
    ups.append(up)
    rank = 0
    if isPoss:
        rank = checkRank(id)
    return ups,rank

def checkRank(id):
    mysqlconnect = MysqlConnect()
    sql = f"SELECT `Rank` FROM `Up{id}` ORDER BY `Date` DESC;"
    rank = [(Rank) for (Rank,) in mysqlconnect.queryOutCome(sql)]
    #print(rank[0])
    return rank[0]