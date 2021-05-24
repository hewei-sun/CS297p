from pyfiles.WEBuploader import Uploader
from pyfiles.WEBsingleQueries import ifPossible
from pyfiles.MysqlConnect import MysqlConnect

def uploaderAna(id):
    isPoss = ifPossible(id)
    up = Uploader(id,isPoss)
    up.crawl_basic()
    up.crawlMaster()
    ups = []
    ups.append(up)
    rank = 0
    info = []
    if isPoss:
        rank = checkRank(id)
        info = historyInfo(id)
    return ups,rank,info

def checkRank(id):
    mysqlconnect = MysqlConnect()
    sql = f"SELECT `Rank` FROM `Up{id}` ORDER BY `Date` DESC;"
    rank = [(Rank) for (Rank,) in mysqlconnect.queryOutCome(sql)]
    #print(rank[0])
    return rank[0]
    
def historyInfo(id):
    mysqlconnect = MysqlConnect()
    sql = f"SELECT SUBSTRING_INDEX(`Date`,' ',1) AS Date,`Followings`,`Followers`,`Likes`,`Views`,`Rank` FROM `Up{id}` ORDER BY `Date`;"
    infos = [(Date,Followings,Followers,Likes,Views,Rank) for (Date,Followings,Followers,Likes,Views,Rank,) in mysqlconnect.queryOutCome(sql)]
    Date = []
    Followers =[]
    Followings = []
    Likes = []
    Views = []
    Rank = []
    for i in infos:
        Date.append(i[0])
        Followings.append(i[1])
        Followers.append(i[2])
        Likes.append(i[3])
        Views.append(i[4])
        Rank.append(i[5])
    info = []
    info.append(Date)
    info.append(Followings)
    info.append(Followers)
    info.append(Likes)
    info.append(Views)
    info.append(Rank)
    return info