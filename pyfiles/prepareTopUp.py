import requests
import time, random
from MysqlConnect import MysqlConnect
from Spider import Spider
from videoRankings import getURLFormBilibili, prepareAllRankings
from datetime import datetime, timedelta
from math import ceil
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

user_agents=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46']
headers = {'user-agent': random.choice(user_agents),
           'referer': 'https://space.bilibili.com/562197/',
           'Cookie': "DedeUserID__ckMd5=2e697f52386d43f6; _uuid=EF2DAAED-E1B0-1B62-AC90-95FFE33A56CB71197infoc; fts=1531899601; buvid3=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; DedeUserID=7255947; blackside_state=1; rpdid=|(JY~|J)J|RY0J'ullYuuJmRR; CURRENT_FNVAL=80; LIVE_BUVID__ckMd5=97f1fede58a29dba; LIVE_BUVID=51c5671403d1ff3a3002f405d313a243; CURRENT_QUALITY=80; fingerprint=45bff20986aa4242239b29ed097fc9e9; buvid_fp=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; buvid_fp_plain=538F6B2F-C709-4EA9-B284-ACD021EF94AB18531infoc; SESSDATA=9c02010b%2C1628737703%2Cdfaa0%2A21; bili_jct=21e92ad75ec8725e7d1cde39f76d728e; sid=br04i46m; bp_video_offset_7255947=514515577167187812; bfe_id=1bad38f44e358ca77469025e0405c4a6; bp_t_offset_7255947=518631019120005148; PVID=1"
           }
'''

user_agents=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56']
headers = {'user-agent': random.choice(user_agents),
           'referer': 'https://space.bilibili.com/562197/',
           'Cookie':"DedeUserID__ckMd5=2e697f52386d43f6; _uuid=EF2DAAED-E1B0-1B62-AC90-95FFE33A56CB71197infoc; fts=1531899601; buvid3=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; DedeUserID=7255947; blackside_state=1; rpdid=|(JY~|J)J|RY0J'ullYuuJmRR; CURRENT_FNVAL=80; LIVE_BUVID__ckMd5=97f1fede58a29dba; LIVE_BUVID=51c5671403d1ff3a3002f405d313a243; CURRENT_QUALITY=80; fingerprint=45bff20986aa4242239b29ed097fc9e9; buvid_fp=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; buvid_fp_plain=538F6B2F-C709-4EA9-B284-ACD021EF94AB18531infoc; SESSDATA=9c02010b%2C1628737703%2Cdfaa0%2A21; bili_jct=21e92ad75ec8725e7d1cde39f76d728e; sid=br04i46m; bp_video_offset_7255947=514515577167187812; bp_t_offset_7255947=524307801952423267; _dfcaptcha=df276be3f70fc51a9c7c15b154e33825; PVID=1; bfe_id=6f285c892d9d3c1f8f020adad8bed553"}

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

def checkTopUp(url):
    spider = Spider(url,headers)
    spider.setSoup()
    itemList = spider.findTag('p')
    mysqlconnect = MysqlConnect()
    for item in itemList:
        if item.find('a'):
            spaceLink = item.find('a').get('href')
            #print(spaceLink)
            upID = spaceLink[len('https://space.bilibili.com/'):]
            sql = '''SELECT COUNT(`ID`) FROM `PossibleTopUp` WHERE `ID` = {};'''.format(upID)
            (rank) = mysqlconnect.queryOutCome(sql)[0][0]
            if rank == 0:
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
    print(f'Just inserted a new Up {mid} to PossibleTopUp')
    return None

def addPossibleUpFromRanking():
    #tables = ['all', 'guochuang', 'douga', 'music', 'dance', 'game', 'technology', 'digital', 'car', 'life', 'food', 'animal',
             #'kichiku', 'fashion', 'ent', 'cinephile', 'origin', 'rookie']
    tables = ['kichiku', 'rookie']
    missed = []
    mysqlconnect = MysqlConnect()
    random.shuffle(tables)
    for table in tables:
        sql = f'select `Up_ID` from `{table}`;'
        upList = [item for (item,) in mysqlconnect.queryOutCome(sql)]
        print('Start Check UP IDs from ',table,'.')
        random.shuffle(upList)
        for up in upList:
            if up==0:
                continue
            sql = 'SELECT 1 FROM `PossibleTopUp` WHERE `ID`={};'.format(up)
            if mysqlconnect.queryOutCome(sql):  # up existed
                continue
            numFollowings, numFollowers = getFollowersByID(up)
            if (numFollowers == numFollowings == 0):  # Failed to visit the F&F page
                missed.append(up)
                continue
            time.sleep(random.random() * 5)
            if numFollowers >= FAN_LIMIT:
                print("catched one:", up, numFollowers)
                ret = addOnePossibleUp(up, numFollowings, numFollowers)
                if ret: missed.append(ret)
                time.sleep(random.random() * 10)
        time.sleep(random.random() * 10)
    return missed

def crawlFollowingsByID(up, headers, url_head, direction, n):
    # crawl up's following list in `direction` order for `n` people.
    mysqlconnect = MysqlConnect()
    missed = []
    status = True # record whose following list page have not been opened successfuly

    visited=0
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
            if up not in missed: missed.append(up)
            status=False
            break
        elif not _json['data']['list']:
            print('Empty Page {}'.format(url))
            break
        for item in _json.get('data').get('list'):
            visited += 1
            mid = item['mid']

            # ------- for following{up} --------------------
            print(f'Adding {mid} into following{up}')
            sql = '''INSERT IGNORE INTO `following{}` VALUES ({});'''.format(up, mid)
            mysqlconnect.insertInfo(sql)

            # ---------- for possibleTopUp ------------------
            sql = 'SELECT 1 FROM `PossibleTopUp` WHERE `ID`={};'.format(mid)
            if mysqlconnect.queryOutCome(sql):  # up existed, skip to the next one
                continue
            numFollowings, numFollowers = getFollowersByID(mid)
            if (numFollowers == numFollowings == 0):  # Failed to visit the F&F page
                missed.append(mid)
                continue
            time.sleep(random.random() * 5)
            if numFollowers >= FAN_LIMIT:
                ret = addOnePossibleUp(mid, numFollowings, numFollowers)
                if ret: missed.append(ret)
            # check whether exceeds n
            if visited >= n:
                break
        else: # Continue if the inner loop wasn't broken.
            time.sleep(random.random() * 10)
            continue
        # Inner loop was broken, break the outer.
        break
    print(f'You just visited {visited} from {up}\'s following list in {direction} order.\n')
    return missed, status

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

    headers = {'referer':'',
               'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46',
               'cookie': "DedeUserID__ckMd5=2e697f52386d43f6; _uuid=EF2DAAED-E1B0-1B62-AC90-95FFE33A56CB71197infoc; fts=1531899601; buvid3=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; DedeUserID=7255947; blackside_state=1; rpdid=|(JY~|J)J|RY0J'ullYuuJmRR; CURRENT_FNVAL=80; LIVE_BUVID__ckMd5=97f1fede58a29dba; LIVE_BUVID=51c5671403d1ff3a3002f405d313a243; CURRENT_QUALITY=80; fingerprint=45bff20986aa4242239b29ed097fc9e9; buvid_fp=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; buvid_fp_plain=538F6B2F-C709-4EA9-B284-ACD021EF94AB18531infoc; SESSDATA=9c02010b%2C1628737703%2Cdfaa0%2A21; bili_jct=21e92ad75ec8725e7d1cde39f76d728e; sid=br04i46m; bp_video_offset_7255947=514515577167187812; bfe_id=1bad38f44e358ca77469025e0405c4a6; bp_t_offset_7255947=518631019120005148; PVID=2"
               }
    '''
    headers = {'referer': '',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
               'cookie': "DedeUserID__ckMd5=2e697f52386d43f6; _uuid=EF2DAAED-E1B0-1B62-AC90-95FFE33A56CB71197infoc; fts=1531899601; buvid3=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; DedeUserID=7255947; blackside_state=1; rpdid=|(JY~|J)J|RY0J'ullYuuJmRR; CURRENT_FNVAL=80; LIVE_BUVID__ckMd5=97f1fede58a29dba; LIVE_BUVID=51c5671403d1ff3a3002f405d313a243; CURRENT_QUALITY=80; fingerprint=45bff20986aa4242239b29ed097fc9e9; buvid_fp=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; buvid_fp_plain=538F6B2F-C709-4EA9-B284-ACD021EF94AB18531infoc; SESSDATA=9c02010b%2C1628737703%2Cdfaa0%2A21; bili_jct=21e92ad75ec8725e7d1cde39f76d728e; sid=br04i46m; bp_video_offset_7255947=514515577167187812; bp_t_offset_7255947=524307801952423267; _dfcaptcha=df276be3f70fc51a9c7c15b154e33825; PVID=1; bfe_id=6f285c892d9d3c1f8f020adad8bed553"
               }

    missed = []
    missed_add_following = []
    mysqlconnect=MysqlConnect()
    sql = "SELECT `ID`, `Followings` FROM `NewestTop100`"
    upList = [(up, numFollowings) for (up,numFollowings,) in mysqlconnect.queryOutCome(sql)]
    random.shuffle(upList)
    for up, numFollowings in upList:
    #for up, numFollowings in [(258150656, 51)]:
        headers['referer']='https://space.bilibili.com/{}/fans/follow'.format(up)
        url_head = f'https://api.bilibili.com/x/relation/followings?vmid={up}&'

        sql1 = f'SHOW TABLES LIKE \"Up{up}\";' # In case we missed creating an individual table for some top100
        tableExisted = mysqlconnect.queryOutCome(sql1)
        numRows = 0
        if tableExisted:
            sql2 = f'SELECT COUNT(*) FROM Up{up};' # In case the Up is added to PossibleTop yesterday, we have not fully crawled his/her following list yet.
            (numRows,) = mysqlconnect.queryOutCome(sql2)[0]

        todayFollowings, todayFollowers = getFollowersByID(up)
        if numRows>=2: # only crawl the new followings
            todayFollowings, todayFollowers = getFollowersByID(up)
            print(f"Up {up} has {numFollowings} followings yestoday and {todayFollowings} today.")
            if todayFollowings-numFollowings>0:
                tmp1, tmp2 = crawlFollowingsByID(up, headers, url_head, 'desc', todayFollowings-numFollowings)
                missed += tmp1
                if tmp2==False: missed_add_following.append(up)

        else: # This up's following list has not been fully crawled, need to do that
            sql = '''CREATE TABLE IF NOT EXISTS `{}`
                                    (
                                        `ID` INT UNIQUE,
                                         PRIMARY KEY(ID)
                                    )ENGINE=innodb DEFAULT CHARSET=utf8;'''.format('following' + str(up))
            mysqlconnect.queryOutCome(sql)
            print(f'This is the first time to crawl Up {up}\'s following list.')
            tmp1, tmp2 = crawlFollowingsByID(up, headers, url_head, 'desc', todayFollowings - numFollowings)
            missed += tmp1
            if tmp2 == False: missed_add_following.append(up)

            todayFollowings -= 250
            if todayFollowings > 0:  # crawl from the reverse direction but only took first `remaining` ones
                tmp1, tmp2 = crawlFollowingsByID(up, headers, url_head, 'desc', todayFollowings - numFollowings)
                missed += tmp1
                if tmp2 == False: missed_add_following.append(up)

    print('finished up ', up,'\n')
    print('Failed to crawl these Ups:', missed)
    print('Failed to visit these Ups\' full following list page(s):', missed_add_following )
    return missed, missed_add_following

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
        sql = '''DROP TABLE IF EXISTS {} ;'''.format('following'+str(up))
        mysqlconnect.queryOutCome(sql)

def recover():
    # If dropped the PossibleTopUp by accidently, use below code
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES;'
    upList = [tb[2:] for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:2]=='Up']
    refreshPossibleTopUp(upList)

def dropfirst():
    # --------- Use below code to drop the latest row of Up table----------------------
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES'
    upList = [tb[2:] for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:2] == 'Up']
    print(upList)
    for up in upList:
        sql = f"DELETE FROM `Up{up}` ORDER BY `Date` DESC LIMIT 1;"
        print(mysqlconnect.queryOutCome(sql))

def fixTimeLag():
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES'
    upList = [tb[2:] for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:2] == 'Up']
    print(len(upList))
    for up in upList:
        sql = f"SELECT `Date` FROM `Up{up}` ORDER BY `Date` DESC LIMIT 1,1;"
        old_date = mysqlconnect.queryOutCome(sql)[0][0]
        print("old", old_date)
        new_date = old_date + timedelta(hours=15)
        print('new', new_date)
        sql = f"UPDATE `Up{up}` SET `Date` = '{new_date}' WHERE `Date` = '{old_date}';"
        print(mysqlconnect.queryOutCome(sql))

def fixPartialUp():
    mysqlconnect = MysqlConnect()
    sql = 'SELECT table_name FROM information_schema.TABLES'
    upList = [tb[2:] for (tb,) in mysqlconnect.queryOutCome(sql) if tb[0:2] == 'Up']
    for up in upList:
        sql = f"SELECT FROM `Up{up}` ORDER BY `Date` DESC LIMIT 1;"

if __name__ == "__main__":

    print(datetime.now())
    # initialTop100('https://www.bilibili.com/read/cv10601513')
    # updateTop100()

    # checkTopUp('https://www.bilibili.com/read/cv11147845')
    # print("done check")

    # --------- Call below every day ----------------------

    # 1. crawl up following and add to list
    crawlUp, addUp = crawlUpFollowing()
    if len(addUp) != 0:
        with open("AddMissed.txt", 'a+') as f:
            for up in addUp:
                f.write(str(up) + "\n")

    if len(crawlUp) != 0:
        with open("crawlMissed.txt", 'a+') as f:
            for up in crawlUp:
                f.write(str(up) + "\n")
        print('------------You need to Repeat from Step 1.----------------')
        exit()
    print('Added PossibleTopUp from Following Lists.')
    
    # 2. Crawl Today's videos rankings and save them into database
    print("Cooling for 30 mins.")
    time.sleep(1800)  # stop for 30 min
    prepareAllRankings()
    print("Saved Hot Videos Ranks")
    
    # 3. Add new ones into PossibleTopUP via today's video ranking
    print("Cooling for 30 mins.")
    time.sleep(1800)  # stop for 30 min
    rankUp = addPossibleUpFromRanking()
    if len(rankUp) != 0:
        with open("rankMissed.txt", 'a+') as f:
            for up in rankUp:
                f.write(str(up) + "\n")
        print('------------You need to Repeat from Step 3.----------------')
        exit()
    print('Added PossibleTopUp from Hot Videos Rankings.')

    # 4. Refresh PossibleTopUp
    print("Cooling for 30 mins.")
    time.sleep(1800)  # stop for 30 min
    refreshUp = refreshPossibleTopUp()
    if len(refreshUp) != 0:
        with open("refreshMissed.txt", 'a+') as f:
            for up in refreshUp:
                f.write(str(up) + "\n")
        print('----------------You need to call recover() and then start from step 5.----------------')
        exit()
    print('Refreshed PossibledTopUp.')

    # 5. Update Top100 according to newst possibleTopUp
    updateTop100()

    # 6. Collect today's date's data for every top100 Up
    mysqlconnect = MysqlConnect()
    sql = "SELECT `ID` from `PossibleTopUp`;"
    upList = [up for (up,) in mysqlconnect.queryOutCome(sql)]
    print(upList)
    for up in upList:
        #updateUpByDate(up, str(datetime.now()))
        updateUpByDate(up, str(datetime.now() + timedelta(hours=15)))

    print(datetime.now())

