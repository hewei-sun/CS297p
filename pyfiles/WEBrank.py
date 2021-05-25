from pyfiles.MysqlConnect import MysqlConnect
from pyfiles.WEBuploader import Uploader
from pyfiles.WEBvideo import Video
from pyfiles.WEBconvert import img_deal,cover_deal
from pyfiles.WEBrefresh import refreshUpRank,refreshVideoRank
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
    refreshVideoRank()
    mysqlconnect = MysqlConnect()
    sql = "SELECT `Rank`,`ID`,`Name`,`Sex`,`Face`,`Birthday`,`Place`,`Followings`,`Followers`,`Sign`,`Level`,`Official`,`Likes`,`Views` from `NewestTop100` ORDER BY `Rank`;"
    upList = [(Rank,ID,Name,Sex,Face,Birthday,Place,Followings,Followers,Sign,Level,Official,Likes,Views) for (Rank,ID,Name,Sex,Face,Birthday,Place,Followings,Followers,Sign,Level,Official,Likes,Views,) in mysqlconnect.queryOutCome(sql)]
    for up in upList:
        directory = 'static/upFaces/'+str(up[1])+'.png'
        if not os.path.exists(directory):
            img_deal(up[4],directory)
    return upList
    
def webVideoRank(fields):
    mysqlconnect = MysqlConnect()
    sql = f"SELECT `Rank`,`Title`,`BVid`,`Play`,`View`,`Up`,`Up_ID`,`Cover_URL` from `{fields}` ORDER BY `Rank`;"
    vList = [(Rank,Title,BVid,Play,View,Up,Up_ID,Cover_URL) for (Rank,Title,BVid,Play,View,Up,Up_ID,Cover_URL,) in mysqlconnect.queryOutCome(sql)]
    for v in vList:
        directory = 'static/videoFaces/'+str(v[2])+'.png'
        if not os.path.exists(directory):
            cover_deal(v[-1],directory)
    #print(vList)
    return vList

def wreVideoRank(fields):
    refreshVideoRank(fields[4:])

if __name__ == "__main__":
    uplist = webUpRank()
    uplist = json.dumps(uplist)
    print(uplist)