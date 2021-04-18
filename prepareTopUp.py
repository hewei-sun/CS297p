import requests
import time, random
from datetime import datetime
from MysqlConnect import MysqlConnect
from Spider import Spider

user_agents=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36']
'''
['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3']
 '''

headers = {'user-agent':random.choice(user_agents),
           'referer':'https://space.bilibili.com/399966183'}

cookie = {'Cookie' : "_uuid=21EB14CF-CBA0-6FDC-821F-D68A14A5C51409351infoc; "
                     "buvid3=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                     "CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|Jkm|)R|l0J'uYu~Jm)~J); "
                     "fingerprint=760a6edb8fa7f49e216ee581b4c60ece; "
                     "buvid_fp=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                     "buvid_fp_plain=04D4D127-D90F-4AE0-9D9B-DC8F95DD365918550infoc; "
                     "SESSDATA=6ed6c81c,1632952648,72649*41; "
                     "bili_jct=e745c5f985c8e918670d7090d9443ae0; "
                     "DedeUserID=19667955; DedeUserID__ckMd5=00a94d7f3200fdb4; "
                     "sid=9b4dr68a; bsource=search_google; "
                     "PVID=1; bfe_id=1bad38f44e358ca77469025e0405c4a6"}

def getFollowersByID(userID): # return numFollowings and numFollowers
    url = f'https://api.bilibili.com/x/relation/stat?vmid={userID}&jsonp=jsonp'
    try:
        r = requests.session().get(url, headers=headers, cookies=cookie, timeout=1.5)
        json = r.json()
        numFollowings, numFollowers = json['data']['following'], json['data']['follower']
        return numFollowings, numFollowers
    except:
        return "Sorry, due to some reason, you failed to visit the page.\n{}".format(url)

def getLikesByID(userID): # return numLikes and numViews
    url = f'https://api.bilibili.com/x/space/upstat?mid={userID}&jsonp=jsonp'
    try:
        r = requests.session().get(url, headers=headers, cookies=cookie, timeout=1.5)
        json = r.json()
        numLikes, numViews = json['data']['likes'], json['data']['archive']['view']
        return numLikes, numViews
    except:
        return "Sorry, due to some reason, you failed to visit the page.\n{}".format(url)


# Prepare table 1 from https://www.bilibili.com/read/cv10601513
def initialTop100(url): # Only called at Day 1
    spider = Spider(url, headers)
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
            numLikes, numViews = getLikesByID(upID)
            #print(numFollowings, numFollowers, numLikes, numViews)
            sql = mysqlconnect.getInsertToTable1Sql('PossibleTopUp', upID, numFollowings, numFollowers, numLikes, numViews)
            mysqlconnect.insertInfo(sql)


# Refresh Up's 4 data in possibleTopUp
def refreshPossibleTopUp():
    mysqlconnect = MysqlConnect()
    mysqlconnect.getConnect()
    sql = "SELECT `ID` FROM `PossibleTopUp`"
    upList = [item for (item,) in mysqlconnect.queryOutCome(sql)]
    mysqlconnect.createTable1()  # delete the old table, create a new one
    random.shuffle(upList)
    for upID in upList:
        numFollowings, numFollowers = getFollowersByID(upID)
        numLikes, numViews = getLikesByID(upID)
        sql = mysqlconnect.getInsertToTable1Sql('PossibleTopUp', upID, numFollowings, numFollowers, numLikes, numViews)
        mysqlconnect.insertInfo(sql)


# Add UPs whose followers exceeds FAN_LIMIT to the table PossibleTopUp
FAN_LIMIT=1000000
def crawlUpFollowing():
    cookies={'Cookie' : "_uuid=21EB14CF-CBA0-6FDC-821F-D68A14A5C51409351infoc; "
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
                         "bfe_id=603589b7ce5e180726bfa88808aa8947"}
    headers = {'referer':'https://space.bilibili.com/399966183/fans/follow',
               'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/89.0.4389.114 Safari/537.36'}
    missed = []
    mysqlconnect=MysqlConnect()
    mysqlconnect.getConnect()
    sql = "SELECT `ID` FROM `PossibleTopUp`"
    upList = [item for (item,) in mysqlconnect.queryOutCome(sql)]
    random.shuffle(upList)
    for up in upList:
        for i in range(1,6):
            url = f'https://api.bilibili.com/x/relation/followings?vmid={up}&pn={i}&ps=20&order=desc&jsonp=jsonp'
            print(url)
            _json = requests.session().get(url, headers=headers, cookies=cookies, timeout=1.5).json()
            if _json['message']=="用户已设置隐私，无法查看" :
                print('用户{}已设置隐私，无法查看'.format(up))
                break
            elif not _json['data']['list']:
                print('Empty Page')
                break
            elif _json['data']==None:
                print('Failed of visiting page.')
                break
            for item in _json.get('data').get('list'):
                mid = item['mid']
                sql = 'SELECT 1 FROM `PossibleTopUp` WHERE `ID`={};'.format(mid)
                if mysqlconnect.queryOutCome(sql): # up existed
                    continue
                numFollowings, numFollowers = getFollowersByID(mid)
                time.sleep(random.random())
                if numFollowers>=FAN_LIMIT:
                    numLikes, numViews = getLikesByID(mid)
                    sql = '''INSERT IGNORE INTO `PossibleTopUp` 
                    VALUES ('{}','{}','{}','{}','{}');'''.format(mid, numFollowings, numFollowers, numLikes, numViews)
                    mysqlconnect.queryOutCome(sql)
                time.sleep(random.random()*5)
            time.sleep(random.random()*6)
        print('Finish Up {}'.format(up))
        time.sleep(random.random()*7)
    print(missed)

def updateTop100():
    mysqlconnect = MysqlConnect()
    mysqlconnect.getConnect()
    mysqlconnect.createTable2()
    sql = "SELECT `ID` from `PossibleTopUp` ORDER BY `Followers` DESC;"
    upList = [item for (item,) in mysqlconnect.queryOutCome(sql)[:100]]
    for id in upList:
        sql = mysqlconnect.getInsertToTable2Sql('NewestTop100', id)
        mysqlconnect.insertInfo(sql)

def updateUpByDate(upID, date):
    mysqlconnect = MysqlConnect()
    mysqlconnect.getConnect()
    sql = '''CREATE TABLE IF NOT EXISTS `{}`
                        (
                            `Date` VARCHAR(60) UNIQUE,
                            `Followings` VARCHAR(40), 
                            `Followers` VARCHAR(40),
                            `Likes` VARCHAR(40),
                            `Views` VARCHAR(40),
                             PRIMARY KEY(Date)
                        )ENGINE=innodb DEFAULT CHARSET=utf8;'''.format('Up'+upID)
    mysqlconnect.queryOutCome(sql)
    sql = '''SELECT `Followings`, `Followers`, `Likes`, `Views` FROM `PossibleTopUp` WHERE `ID`={};'''.format(upID)
    (numFollowings, numFollowers, numLikes, numViews) = mysqlconnect.queryOutCome(sql)[0]
    sql = '''INSERT IGNORE INTO `{}` VALUES ('{}','{}','{}','{}','{}');'''.format('Up'+upID, date, numFollowings, numFollowers, numLikes, numViews)
    print(sql)
    mysqlconnect.queryOutCome(sql)


if __name__ == "__main__":
    #initialTop100('https://www.bilibili.com/read/cv10601513')

    # --------- Call below every day ----------------------
    # 1. Refresh PossibleTopUp
    #refreshPossibleTopUp()
    # 2. Crawl NewestTop100's following, add newly added one into PossibleTopUP
    crawlUpFollowing()
    # 3. Update Top100
    #updateTop100()
    # 4. Collect today's date's data for every top100 Up
    '''
    mysqlconnect = MysqlConnect()
    mysqlconnect.getConnect()
    sql = "SELECT `ID` from `NewestTop100`;"
    upList = [up for (up,) in mysqlconnect.queryOutCome(sql)]
    print(upList)
    for up in upList:
        #sql = "DROP TABLE IF EXISTS `UP{}`;".format(up)
        #mysqlconnect.queryOutCome(sql)
        updateUpByDate(up, str(datetime.now().date()))
    '''

