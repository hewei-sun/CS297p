from pyfiles.videoRankings import prepareOneRanking
from pyfiles.MysqlConnect import MysqlConnect
from pyfiles.Uploader import Uploader
from WEBconvert import cover_deal
import time, random
from datetime import datetime
import requests

user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62']
headers = {'user-agent': random.choice(user_agents),
           'Cookie': "DedeUserID__ckMd5=2e697f52386d43f6; _uuid=EF2DAAED-E1B0-1B62-AC90-95FFE33A56CB71197infoc; fts=1531899601; buvid3=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; DedeUserID=7255947; blackside_state=1; rpdid=|(JY~|J)J|RY0J'ullYuuJmRR; CURRENT_FNVAL=80; LIVE_BUVID__ckMd5=97f1fede58a29dba; LIVE_BUVID=51c5671403d1ff3a3002f405d313a243; CURRENT_QUALITY=80; fingerprint=45bff20986aa4242239b29ed097fc9e9; buvid_fp=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; buvid_fp_plain=538F6B2F-C709-4EA9-B284-ACD021EF94AB18531infoc; SESSDATA=9c02010b%2C1628737703%2Cdfaa0%2A21; bili_jct=21e92ad75ec8725e7d1cde39f76d728e; sid=br04i46m; PVID=1; bp_video_offset_7255947=525371403363400156; bfe_id=cade757b9d3229a3973a5d4e9161f3bc; bp_t_offset_7255947=526517094477426377"}

def getFollowersByID(userID):  # return numFollowings and numFollowers
    url = f'https://api.bilibili.com/x/relation/stat?vmid={userID}&jsonp=jsonp'
    r = ''
    try:
        r = requests.session().get(url, timeout=5)
        json = r.json()
        if not json['data']:
            print('Banned at {}'.format(url))
        numFollowings, numFollowers = json['data']['following'], json['data']['follower']
        return numFollowings, numFollowers
    except:
        if r: print(r.text)
        print("Sorry, due to some reason, you failed to visit the page.\t{}".format(url))
        return 0, 0

def getLikesByID(userID):  # return numLikes and numViews
    url = f'https://api.bilibili.com/x/space/upstat?mid={userID}&jsonp=jsonp'
    r = ''
    try:
        r = requests.session().get(url, headers=headers, timeout=5)
        json = r.json()
        if not json['data']:
            print('Banned at {}'.format(url))
        numLikes, numViews = json['data']['likes'], json['data']['archive']['view']
        return numLikes, numViews
    except:
        if r: print(r.text)
        print("Sorry, due to some reason, you failed to visit the page.\t{}".format(url))
        return 0, 0

def refreshVideoRank(field): # refresh hot 100 video rank in the `field`
    url = 'https://www.bilibili.com/v/popular/rank/{}'.format(field)
    prepareOneRanking(field, url)

'''
DROP TABLE IF EXISTS TESTnewestTop100;
create table TESTnewestTop100 like NewestTop100;
insert into TESTnewestTop100 select * from NewestTop100;
'''
def refreshUpRank(range=105): # refresh top 100 up rank
    mysqlconnect = MysqlConnect()
    sql = f"SELECT `ID` from `PossibleTopUp` ORDER BY `Followers` DESC LIMIT {range};"
    upList = [id for (id,) in mysqlconnect.queryOutCome(sql)]
    print(len(upList),upList)
    alert = False
    random.shuffle(upList)
    for up in upList:
        sql = f'SELECT 1 FROM `NewestTop100` WHERE `ID`={up};'
        if mysqlconnect.queryOutCome(sql):  # up existed, only need to refresh 4 data
            numFollowing, numFollowers = getFollowersByID(up)
            if numFollowing==numFollowers==0:
                alert = True
                continue
            numLikes, numViews = getLikesByID(up)
            time.sleep(random.random() * 5)
            if numLikes==numViews==0:
                alert = True
                continue
            sql = f'UPDATE `NewestTop100` SET' \
                  f'`Followings` = {numFollowing}, `Followers` = {numFollowers},' \
                  f'`Likes` = {numLikes}, `Views` = {numViews}' \
                  f' WHERE `ID` = {up};'
            #print(sql)
            mysqlconnect.queryOutCome(sql)
        else: # Need to crawl all info
            u = Uploader(up, True)
            u.crawl_basic()
            sql = mysqlconnect.getInsertToTable2Sql('NewestTop100', 0, up, u.name, u.sex, u.birthday, u.place,
                                                    u.level, u.faceURL, u.numFollowings, u.numFollowers, u.numLikes, u.numViews,
                                                    u.sign, u.official)
            #print(sql)
            mysqlconnect.queryOutCome(sql)
        time.sleep(random.random() * 5)

    # drop rows beyond 100
    sql = "SELECT `ID` from `NewestTop100` ORDER BY `Followers` DESC;"
    upList = [id for (id,) in mysqlconnect.queryOutCome(sql)]
    for up in upList[100:]:
        sql = f'DELETE FROM `NewestTop100` WHERE `ID` = {up};'
        mysqlconnect.queryOutCome(sql)
    # update column Rank
    i = 1
    for up in upList[:100]:
        sql = f'UPDATE `NewestTop100` SET `Rank`= {i} WHERE `ID`= {up};'
        i += 1
        mysqlconnect.queryOutCome(sql)
    if alert==True:
        print("Too Frequent Refresh Queries, Please Wait for a While to Proceed Next Refresh.")

def downloadCoversFrom(tableName):
    mysqlconnect = MysqlConnect()
    sql = f'select `BVid`, `Cover_URL` from `{tableName}`;'
    items = [(bvid, url) for (bvid, url,) in mysqlconnect.queryOutCome(sql)]
    for bvid, url in items:
        cover_deal(url, '../static/videoFaces/' + bvid + '.png')

def downloadAllCovers():
    tables = ['RANKall', 'RANKguochuang', 'RANKdouga', 'RANKmusic', 'RANKdance', 'RANKgame', 'RANKtechnology',
              'RANKdigital',
              'RANKcar', 'RANKlife', 'RANKfood', 'RANKanimal', 'RANKkichiku', 'RANKfashion', 'RANKent', 'RANKcinephile',
              'RANKorigin', 'RANKrookie']
    for t in tables:
        downloadCoversFrom(t)


if __name__ == "__main__":
    print(datetime.now())
    #fields = ['all', 'guochuang', 'douga', 'music', 'dance', 'game', 'technology', 'digital',
              #'car', 'life', 'food', 'animal', 'kichiku', 'fashion', 'ent', 'cinephile', 'origin', 'rookie']
    '''
    fields = ['car', 'life', 'food', 'animal', 'kichiku', 'fashion', 'ent', 'cinephile', 'origin', 'rookie']
    for f in fields:
        refreshVideoRank(f)
        print(datetime.now())
    '''
    downloadAllCovers()
    #refreshUpRank()
