from pyfiles.MysqlConnect import MysqlConnect
from pyfiles.WEBuploader import Uploader
from pyfiles.WEBvideo import Video
from pyfiles.WEBconvert import img_deal,cover_deal

def webUpRank():
    mysqlconnect = MysqlConnect()
    sql = "SELECT `ID`,`Followings`,`Rank` from `NewestTop100` ORDER BY `Rank`;"
    upList = [(ID, Followings, Rank) for (ID, Followings, Rank,) in mysqlconnect.queryOutCome(sql)]
    ups = []
    for up in upList:
        UP = Uploader(up[0])
        UP.crawl_basic()
        ups.append(UP.__dict__)
        img_deal(UP.faceURL,'static/upFaces/'+str(UP.uid)+'.png')
    return ups
    
def webVideoRank():
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES'
    field = [tb for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:2] == 'Rank']
    
    videos=[]
    for f in field:
        sql = f"SELECT `Rank`,`Title`,`BVid`,`Play`,`View`,`Up`,`Up_ID`,`Cover_URL` from `{f}` ORDER BY `Rank`;"
        vList = [(Rank,Title,BVid,Play,View,Up,Up_ID,Cover_URL) for (Rank,Title,BVid,Play,View,Up,Up_ID,Cover_URL,) in mysqlconnect.queryOutCome(sql)]
        videos.append(vList)
        for v in vList:
            cover_deal(v[-1],'static/videoFaces/'+str(v[3])+'.png')
        f = f[2:]
    print(field)
    return videos,field

if __name__ == "__main__":
    uplist = webUpRank()
    uplist = json.dumps(uplist)
    print(uplist)