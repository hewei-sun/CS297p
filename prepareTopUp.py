import requests
import time, random
from MysqlConnect import MysqlConnect
from Spider import Spider
from videoRankings import getURLFormBilibili
from datetime import datetime, timedelta
'''
user_agents=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36']
headers = {'user-agent': random.choice(user_agents),
           'referer': 'https://space.bilibili.com/14583962/',
           'Cookie': "_uuid=21EB14CF-CBA0-6FDC-821F-D68A14A5C51409351infoc; "
                     "buvid3=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                     "CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|Jkm|)R|l0J'uYu~Jm)~J); "
                     "fingerprint=760a6edb8fa7f49e216ee581b4c60ece; "
                     "buvid_fp=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                     "buvid_fp_plain=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                     "SESSDATA=6ed6c81c%2C1632952648%2C72649%2A41; "
                     "bili_jct=e745c5f985c8e918670d7090d9443ae0; "
                     "DedeUserID=19667955; DedeUserID__ckMd5=00a94d7f3200fdb4; sid=9b4dr68a; bsource=search_google; "
                     "PVID=1; bfe_id=6f285c892d9d3c1f8f020adad8bed553"
           }
'''
user_agents=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46']
headers = {'user-agent': random.choice(user_agents),
           'referer': 'https://space.bilibili.com/562197/',
           'Cookie': "DedeUserID__ckMd5=2e697f52386d43f6; _uuid=EF2DAAED-E1B0-1B62-AC90-95FFE33A56CB71197infoc; fts=1531899601; buvid3=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; DedeUserID=7255947; blackside_state=1; rpdid=|(JY~|J)J|RY0J'ullYuuJmRR; CURRENT_FNVAL=80; LIVE_BUVID__ckMd5=97f1fede58a29dba; LIVE_BUVID=51c5671403d1ff3a3002f405d313a243; CURRENT_QUALITY=80; fingerprint=45bff20986aa4242239b29ed097fc9e9; buvid_fp=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; buvid_fp_plain=538F6B2F-C709-4EA9-B284-ACD021EF94AB18531infoc; SESSDATA=9c02010b%2C1628737703%2Cdfaa0%2A21; bili_jct=21e92ad75ec8725e7d1cde39f76d728e; sid=br04i46m; bp_video_offset_7255947=514515577167187812; bfe_id=1bad38f44e358ca77469025e0405c4a6; bp_t_offset_7255947=518631019120005148; PVID=1"
           }

def getFollowersByID(userID): # return numFollowings and numFollowers
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
        return 0,0

def getLikesByID(userID): # return numLikes and numViews
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


# Prepare table 1 from https://www.bilibili.com/read/cv10601513
def initialTop100(url): # Only called at Day 1
    spider = Spider(url,headers)
    spider.setSoup()
    itemList = spider.findTag('p')
    mysqlconnect = MysqlConnect()
    mysqlconnect.createTable1() # table1: PossibleTopUp
    for item in itemList:
        if item.find('a'):
            spaceLink = item.find('a').get('href')
            #print(spaceLink)
            upID = spaceLink[len('https://space.bilibili.com/'):]
            numFollowings, numFollowers = getFollowersByID(upID)
            time.sleep(random.random())
            numLikes, numViews = getLikesByID(upID)
            print(upID, numFollowings, numFollowers, numLikes, numViews)
            sql = mysqlconnect.getInsertToTable1Sql('PossibleTopUp', upID, numFollowings, numFollowers, numLikes, numViews)
            mysqlconnect.insertInfo(sql)
        time.sleep(random.random() * 5)


# Refresh Up's 4 data in possibleTopUp
def refreshPossibleTopUp(upList=None):
    missed = []
    mysqlconnect = MysqlConnect()
    if not upList:
        sql = "SELECT `ID` FROM `PossibleTopUp`"
        upList = [item for (item,) in mysqlconnect.queryOutCome(sql)]
    mysqlconnect.createTable1()  # deleted the old table, create a new one
    random.shuffle(upList)
    for upID in upList:
        numFollowings, numFollowers = getFollowersByID(upID)
        if numFollowings==numFollowers==0:
            print("Failed crawling data for up ",upID)
            missed.append(upID)
            continue
        time.sleep(random.random() * 5)
        numLikes, numViews = getLikesByID(upID)
        if numLikes==numViews==0:
            print("Failed crawling data for up ", upID)
            missed.append(upID)
            continue
        sql = mysqlconnect.getInsertToTable1Sql('PossibleTopUp', upID, numFollowings, numFollowers, numLikes, numViews)
        mysqlconnect.insertInfo(sql)
        time.sleep(random.random() * 10)
    return missed

def addOnePossibleUp(mid, numFollowings, numFollowers):
    mysqlconnect = MysqlConnect()
    numLikes, numViews = getLikesByID(mid)
    if (numLikes == numViews == 0):  # Failed to visit the L&V poge
        return mid
    sql = mysqlconnect.getInsertToTable1Sql('PossibleTopUp', mid, numFollowings, numFollowers, numLikes, numViews)
    mysqlconnect.insertInfo(sql)
    return None

def addPossibleUpFromRanking():
    urlDict = getURLFormBilibili()
    mysqlconnect = MysqlConnect()
    missed = []
    for field, url in urlDict.items():
        spider = Spider(url, headers)
        spider.setSoup()
        itemList = spider.findTagByAttrs('li', {'class': 'rank-item'})
        for itm in itemList:
            mid = itm.find('div', {'class': 'detail'}).find('a').get('href')[len('//space.bilibili.com/'):]
            sql = 'SELECT 1 FROM `PossibleTopUp` WHERE `ID`={};'.format(mid)
            if mysqlconnect.queryOutCome(sql):  # up existed
                continue
            numFollowings, numFollowers = getFollowersByID(mid)
            if (numFollowers == numFollowings == 0):  # Failed to visit the F&F page
                missed.append(mid)
                continue
            time.sleep(random.random() * 5)
            if numFollowers >= FAN_LIMIT:
                print("catched one:", mid,numFollowers)
                ret = addOnePossibleUp(mid, numFollowings, numFollowers)
                if ret: missed.append(ret)
            time.sleep(random.random() * 10)
    return missed

def getFollowingsByID(up, headers, url_head, direction, n):
    mysqlconnect = MysqlConnect()
    missed = []
    crawled=0
    for i in range(1, 6):
        url = url_head + f'pn={i}&ps=50&order={direction}&jsonp=jsonp'
        print(url)
        r = requests.session().get(url, headers=headers, timeout=5)
        _json = r.json()
        if _json['message'] == "用户已设置隐私，无法查看":
            print('用户{}已设置隐私，无法查看'.format(up))
            break
        elif not _json['data']:
            print('Failed of visiting page at {}'.format(url), '\n', r.text)
            break
        elif not _json['data']['list']:
            print('Empty Page {}'.format(url))
            break
        for item in _json.get('data').get('list'):
            mid = item['mid']
            sql = 'SELECT 1 FROM `PossibleTopUp` WHERE `ID`={};'.format(mid)
            if mysqlconnect.queryOutCome(sql):  # up existed
                continue
            numFollowings, numFollowers = getFollowersByID(mid)
            if (numFollowers == numFollowings == 0):  # Failed to visit the F&F page
                missed.append(mid)
                continue
            time.sleep(random.random() * 5)
            if numFollowers >= FAN_LIMIT:
                ret = addOnePossibleUp(mid, numFollowings, numFollowers)
                if ret: missed.append(ret)
            crawled += 1
            if crawled==n:
                #print('you crawled',crawled,'ups.')
                break
            time.sleep(random.random() * 10)
        else:
            #time.sleep(random.random() * 10)
            continue
        break
    return missed


# Add UPs whose followers exceeds FAN_LIMIT to the table PossibleTopUp
FAN_LIMIT=1500000
def crawlUpFollowing():
    '''
    headers = {'referer':'',
               'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/89.0.4389.114 Safari/537.36',
               'cookie': "_uuid=21EB14CF-CBA0-6FDC-821F-D68A14A5C51409351infoc; "
                         "buvid3=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                         "CURRENT_FNVAL=80; blackside_state=1; "
                         "rpdid=|(k|Jkm|)R|l0J'uYu~Jm)~J); "
                         "fingerprint=760a6edb8fa7f49e216ee581b4c60ece; "
                         "buvid_fp=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                         "buvid_fp_plain=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                         "SESSDATA=6ed6c81c,1632952648,72649*41; "
                         "bili_jct=e745c5f985c8e918670d7090d9443ae0; "
                         "DedeUserID=19667955; "
                         "DedeUserID__ckMd5=00a94d7f3200fdb4; "
                         "sid=9b4dr68a; bsource=search_google; "
                         "PVID=3; "
                         "bfe_id=603589b7ce5e180726bfa88808aa8947"
               }
    '''
    headers = {'referer':'',
               'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46',
               'cookie': "DedeUserID__ckMd5=2e697f52386d43f6; _uuid=EF2DAAED-E1B0-1B62-AC90-95FFE33A56CB71197infoc; fts=1531899601; buvid3=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; DedeUserID=7255947; blackside_state=1; rpdid=|(JY~|J)J|RY0J'ullYuuJmRR; CURRENT_FNVAL=80; LIVE_BUVID__ckMd5=97f1fede58a29dba; LIVE_BUVID=51c5671403d1ff3a3002f405d313a243; CURRENT_QUALITY=80; fingerprint=45bff20986aa4242239b29ed097fc9e9; buvid_fp=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; buvid_fp_plain=538F6B2F-C709-4EA9-B284-ACD021EF94AB18531infoc; SESSDATA=9c02010b%2C1628737703%2Cdfaa0%2A21; bili_jct=21e92ad75ec8725e7d1cde39f76d728e; sid=br04i46m; bp_video_offset_7255947=514515577167187812; bfe_id=1bad38f44e358ca77469025e0405c4a6; bp_t_offset_7255947=518631019120005148; PVID=2"
               }

    missed = []
    mysqlconnect=MysqlConnect()
    sql = "SELECT `ID`, `Followings` FROM `NewestTop100`"
    upList = [(up, numFollowings) for (up,numFollowings,) in mysqlconnect.queryOutCome(sql)]
    random.shuffle(upList)
    for up, numFollowings in upList:
    #for up, numFollowings in [(946974,352)]:
        headers['referer']='https://space.bilibili.com/{}/fans/follow'.format(up)
        url_head = f'https://api.bilibili.com/x/relation/followings?vmid={up}&'
        missed += getFollowingsByID(up, headers, url_head, 'asc', min(250, numFollowings))
        numFollowings -= 250
        if numFollowings>0: # crawl from the reverse direction but only took first `remaining` ones
            missed += getFollowingsByID(up, headers, url_head, 'desc', min(250,numFollowings))
        print('finished up ', up)
    print('Failed to crawl these Ups:', missed)
    return missed

def updateTop100():
    mysqlconnect = MysqlConnect()
    mysqlconnect.createTable2()
    sql = "SELECT `ID`, `Followings` from `PossibleTopUp` ORDER BY `Followers` DESC;"
    upList = [(id, numFollowings) for (id, numFollowings,) in mysqlconnect.queryOutCome(sql)[:100]]
    print(upList)
    rank = 1
    for id,numFollowings in upList:
        sql = mysqlconnect.getInsertToTable2Sql('NewestTop100', id, rank, numFollowings)
        mysqlconnect.insertInfo(sql)
        rank += 1

def updateUpByDate(upID, date):
    mysqlconnect = MysqlConnect()
    sql = '''CREATE TABLE IF NOT EXISTS `{}`
                        (
                            `Date` DATETIME UNIQUE,
                            `Followings` INT, 
                            `Followers` BIGINT,
                            `Likes` BIGINT,
                            `Views` BIGINT,
                            `Rank` INT,
                             PRIMARY KEY(Date)
                        )ENGINE=innodb DEFAULT CHARSET=utf8;'''.format('Up'+str(upID))
    mysqlconnect.queryOutCome(sql)
    sql = '''SELECT `Followings`, `Followers`, `Likes`, `Views` FROM `PossibleTopUp` WHERE `ID`={};'''.format(upID)
    (numFollowings, numFollowers, numLikes, numViews) = mysqlconnect.queryOutCome(sql)[0]
    sql2 = '''SELECT COUNT(`Rank`) FROM `NewestTop100` WHERE `ID` = {};'''.format(upID)
    (rank) = mysqlconnect.queryOutCome(sql2)[0][0]
    if rank != 0:
        sql2 = '''SELECT `Rank` FROM `NewestTop100` WHERE `ID` = {};'''.format(upID)
        (rank) = mysqlconnect.queryOutCome(sql2)[0][0]
    sql = '''INSERT IGNORE INTO `{}` VALUES ('{}', {}, {}, {}, {},{});'''.format('Up'+str(upID), date, numFollowings, numFollowers, numLikes, numViews, rank)
    print(sql)
    mysqlconnect.queryOutCome(sql)

# drop an Up's row
def dropAll():
    mysqlconnect = MysqlConnect()
    sql = "SELECT `ID` from `PossibleTopUp`;"
    upList = [up for (up,) in mysqlconnect.queryOutCome(sql)]
    for up in upList:
        sql = '''DROP TABLE {};'''.format('Up'+str(up))
        mysqlconnect.queryOutCome(sql)

def recover():
    # If dropped the PossibleTopUp by accidently, use below code
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES'
    upList = [tb[2:] for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:2]=='Up']
    refreshPossibleTopUp(upList)

if __name__ == "__main__":
    print(datetime.now())
    #initialTop100('https://www.bilibili.com/read/cv10601513')
    #updateTop100()
    
    # --------- Call below every day ----------------------
    # 1. Refresh PossibleTopUp
    #refreshPossibleTopUp()
    print('Refreshed PossibledTopUp')
    #time.sleep(1800) # stop for 10 min
    
    # 2. Add new ones into PossibleTopUP via TOP100's following list and today's video ranking
    addPossibleUpFromRanking()
    print('Added PossibleTopUp from Hot Videos Rankings')
    #time.sleep(1800) # stop for 30 min
    #crawlUpFollowing()
    print('Added PossibleTopUp from Following Lists')
    # 3. Update Top100 according to newst possibleTopUp
    '''
    updateTop100()
    # 4. Collect today's date's data for every top100 Up
    mysqlconnect = MysqlConnect()
    sql = "SELECT `ID` from `PossibleTopUp`;"
    upList = [up for (up,) in mysqlconnect.queryOutCome(sql)]
    #print(upList)
    for up in upList:
        #sql = "DROP TABLE IF EXISTS `UP{}`;".format(up)
        #mysqlconnect.queryOutCome(sql)
        #updateUpByDate(up, str(datetime.now().date()))
        updateUpByDate(up, str(datetime.now()))
        #updateUpByDate(up, str(datetime.now() + timedelta(hours=15)))
    '''
    print(datetime.now())