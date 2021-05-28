import time
import requests
from pyfiles.WEBvideo import Video
from pyfiles.Spider import Spider
from collections import Counter
import random
from pyfiles.MysqlConnect import MysqlConnect
from pyfiles.WEBconvert import img_deal
'''
user_agents='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'

user_agents='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62'
headers = {'user-agent': user_agents,
           'referer': ''}
'''        
user_agents=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62']
headers = {'user-agent': random.choice(user_agents),
           'referer': 'https://space.bilibili.com/562197/',
           'Cookie':"DedeUserID__ckMd5=2e697f52386d43f6; _uuid=EF2DAAED-E1B0-1B62-AC90-95FFE33A56CB71197infoc; fts=1531899601; buvid3=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; DedeUserID=7255947; blackside_state=1; rpdid=|(JY~|J)J|RY0J'ullYuuJmRR; CURRENT_FNVAL=80; LIVE_BUVID__ckMd5=97f1fede58a29dba; LIVE_BUVID=51c5671403d1ff3a3002f405d313a243; CURRENT_QUALITY=80; fingerprint=45bff20986aa4242239b29ed097fc9e9; buvid_fp=1FE86BE0-86E5-4443-9EAA-B4692C34CAB24610infoc; buvid_fp_plain=538F6B2F-C709-4EA9-B284-ACD021EF94AB18531infoc; SESSDATA=9c02010b%2C1628737703%2Cdfaa0%2A21; bili_jct=21e92ad75ec8725e7d1cde39f76d728e; sid=br04i46m; bp_video_offset_7255947=525371403363400156; bp_t_offset_7255947=526517094477426377; bfe_id=1bad38f44e358ca77469025e0405c4a6; PVID=2"}

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

class Uploader:
    def __init__(self, uid=None, inPossibleTopUp=False):
        self.uid = uid
        self.inPossibleTopUp = inPossibleTopUp  # False indicates not top100 or unknown yet

        self.name = None 
        self.sex = None
        self.birthday = None
        self.place = None
        self.level = None
        self.faceURL = None

        self.numFollowers = None
        self.numFollowings = None
        self.numLikes = None
        self.numViews = None

        self.sign = None
        self.official = None

        self.masterPieces = [] # 代表作
        self.tags = Counter()  # Count the tag name from history videoList
        self.historyVideos = [] # 历史投稿

    def __str__(self):
        str = '% % % % % % % % % % % % Card % % % % % % % % % % % %\n'
        str += f'ID: {self.uid}\nName: {self.name}\nSex: {self.sex}\nfaceURL: {self.faceURL}\n'\
               f'Birthday: {self.birthday}\nPlace: {self.place}\nNO. Followers: {self.numFollowers}\nNO. Followings: {self.numFollowings}\n'\
               f'Sign: {self.sign}\nLevel: {self.level}\nOfficial: {self.official}'\
               f'NO. Likes: {self.numLikes}\nNO. Views: {self.numViews}\nTags: {self.tags.__str__()}'
        str += '\n% % % % % % % % % % % % % % % % % % % % % % % % % % %\n'
        return str

    def crawl_basic(self):
        headers['referer'] = f'https://space.bilibili.com/{self.uid}'
        url = f'https://api.bilibili.com/x/web-interface/card?mid={self.uid}&jsonp=jsonp&article=true'
        print(url)
        _json = requests.session().get(url, headers=headers, timeout=5).json()
        card = _json['data']['card']
        self.name = card['name']
        if card['sex']=='男':
            self.sex = 'Male'
        elif card['sex']=='女':
            self.sex = 'Female'
        else:
            self.sex = 'N/A'
        self.faceURL = card['face']
        img_deal(self.faceURL, 'static/cupFaces/'+str(self.uid)+'.png')
        self.birthday = card['birthday']
        self.place = card['place']

        self.numFollowers = card['fans']
        self.numFollowings = card['attention']

        if self.inPossibleTopUp:
            mysqlconnect = MysqlConnect()
            sql = 'SELECT `Likes`, `Views` FROM `PossibleTopUp` WHERE `ID`={};'.format(self.uid)
            self.numLikes, self.numViews = mysqlconnect.queryOutCome(sql)[0]
        else:
            self.numLikes, self.numViews = getLikesByID(self.uid)

        self.sign = card['sign']
        self.level = card['level_info']['current_level']
        if card['Official']:
            self.official = card['Official']['title'] + '\n' + card['Official']['desc']

    def extract_videoInfo1(self, dict): # used to collect master piece
        v = Video()
        v.tname = dict['tname']
        v.cover_url = dict['pic']
        v.title = dict['title']
        pubdate = dict['pubdate']
        timeArray = time.localtime(pubdate)
        v.publish_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        v.description = dict['desc']
        v.title = dict['title']
        v.duration = dict['duration']
        stat = dict['stat']
        v.play = stat['view']
        v.view = stat['danmaku']
        v.reply = stat['reply']
        v.collect = stat['favorite']
        v.coin = stat['coin']
        v.share = stat['share']
        v.bvid = dict['bvid']
        print('\n% % % % % % Masterpieces % % % % % %\n')
        v.printInfo()
        print('\n% % % % % % % % % % % % % % % % % %\n')
        return v

    def extract_videoInfo2(self, dict): # used to collect normal history video
        v = Video()
        v.reply = dict['comment']
        v.play = dict['play']
        v.cover_url=dict['pic']
        v.description = dict['description']
        v.title = dict['title']
        pubdate = dict['created']
        timeArray = time.localtime(pubdate)
        v.publish_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        v.duration = dict['length']
        v.view = dict['video_review']
        v.bvid = dict['bvid']
        print('\n% % % % % % History Video % % % % % %\n')
        v.printInfo()
        print('\n% % % % % % % % % % % % % % % % % % %\n')
        return v

    def crawlMaster(self):
        mpURL = f'https://api.bilibili.com/x/space/masterpiece?vmid={self.uid}&jsonp=jsonp'
        _json = requests.session().get(mpURL, headers=headers, timeout=5).json()
        data = _json['data']
        for v in data:
            self.masterPieces.append(self.extract_videoInfo1(v))
    
    def crawlHistory(self):
        pgn = 1
        while True:
            hvURL = f'https://api.bilibili.com/x/space/arc/search?mid={self.uid}&pn={pgn}&ps={20}&jsonp=jsonp'
            _json = requests.session().get(hvURL, headers=headers, timeout=5).json()
            dict = _json['data']['list']
            if not dict['vlist']: break
            if pgn==1: #collect tag names
                for key,val in dict['tlist'].items():
                    self.tags[val['name']] += val['count']
            for item in dict['vlist']:
                self.historyVideos.append(self.extract_videoInfo2(item))
            pgn += 1
       
    def return4data(self):
        if not self.inPossibleTopUp:
            print("Sorry we currently do not have this Up's history Data.")
            return

        mysqlconnect = MysqlConnect()
        sql = f"SELECT `Date`, `Followings`, `Followers`, `Likes`, `Views`, `Rank` from `Up{self.uid}`;"
        date, followings, followers, likes, views, rank = [], [], [], [], [], []
        table = mysqlconnect.queryOutCome(sql)
        for row in table:
            date.append(row[0].strftime("%Y-%m-%d"))
            followings.append(row[1])
            followers.append(row[2])
            likes.append(row[3])
            views.append(row[4])
            rank.append(row[5])

        sql = f'SELECT 1 FROM `NewestTop100` WHERE `ID`={self.uid};'
        if mysqlconnect.queryOutCome(sql):
            return date, followings, followers, likes, views, rank
        else:
            return date, followings, followers, likes, views


if __name__ == "__main__":
    # https: // space.bilibili.com / 5970160
    #up = Uploader(5970160)
    up = Uploader(208259)
    up.crawl_basic()
    #up.crawl_videoList()
    print(up)