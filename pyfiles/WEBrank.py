from pyfiles.MysqlConnect import MysqlConnect
from pyfiles.WEBuploader import Uploader
from pyfiles.WEBvideo import Video
from pyfiles.WEBconvert import img_deal,cover_deal
import os

def webUpRank():
    mysqlconnect = MysqlConnect()
    sql = "SELECT `Rank`,`ID`,`Name`,`Sex`,`Face`,`Birthday`,`Place`,`Followings`,`Followers`,`Sign`,`Level`,`Official`,`Likes`,`Views` from `NewestTop100` ORDER BY `Rank`;"
    upList = [(Rank,ID,Name,Sex,Face,Birthday,Place,Followings,Followers,Sign,Level,Official,Likes,Views) for (Rank,ID,Name,Sex,Face,Birthday,Place,Followings,Followers,Sign,Level,Official,Likes,Views,) in mysqlconnect.queryOutCome(sql)]
    for up in upList:
        directory = 'static/upFaces/'+str(up[1])+'.png'
        if not os.path.exists(directory):
            img_deal(up[4],directory)
    return upList

def wreUpRank():
    #todo
    '''
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
    '''
    return []
    
def webVideoRank():
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES'
    field = [tb[4:] for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:4] == 'RANK']
    
    videos=[]
    for f in field:
        sql = f"SELECT `Rank`,`Title`,`BVid`,`Play`,`View`,`Up`,`Up_ID`,`Cover_URL` from `RANK{f}` ORDER BY `Rank`;"
        vList = [(Rank,Title,BVid,Play,View,Up,Up_ID,Cover_URL) for (Rank,Title,BVid,Play,View,Up,Up_ID,Cover_URL,) in mysqlconnect.queryOutCome(sql)]
        videos.append(vList)
        '''
        for v in vList:
            if v[-1] == "None":
                continue
            cover_deal(v[-1],'static/videoFaces/'+str(v[3])+'.png')
        '''
    return videos,field,field[0]

def wreVideoRank(fields):
    #todo:refresh
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES'
    field = [tb[4:] for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:4] == 'RANK']
    
    videos=[]
    for f in field:
        sql = f"SELECT `Rank`,`Title`,`BVid`,`Play`,`View`,`Up`,`Up_ID`,`Cover_URL` from `RANK{f}` ORDER BY `Rank`;"
        vList = [(Rank,Title,BVid,Play,View,Up,Up_ID,Cover_URL) for (Rank,Title,BVid,Play,View,Up,Up_ID,Cover_URL,) in mysqlconnect.queryOutCome(sql)]
        videos.append(vList)
        '''
        for v in vList:
            if v[-1] == "None":
                continue
            cover_deal(v[-1],'static/videoFaces/'+str(v[3])+'.png')
        '''
    return videos,field,fields

if __name__ == "__main__":
    uplist = webUpRank()
    uplist = json.dumps(uplist)
    print(uplist)