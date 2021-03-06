import time
from Video import Video
import requests
from Spider import Spider
from collections import Counter
from MysqlConnect import MysqlConnect
from WEBconvert import img_deal

user_agents='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
headers = {'user-agent': user_agents,
           'referer': ''}


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

        if _json['message']=='啥都木有':
            print('Page Not Found.\n'
                  'Please check your input, you may entered a non-exsisted Up ID.')
            return False
        if not _json['data']:
            print('Your requests are too frequent, please take a break and come back later.')
            return False

        card = _json['data']['card']
        self.name = card['name']
        if card['sex']=='男':
            self.sex = 'Male'
        elif card['sex']=='女':
            self.sex = 'Female'
        else:
            self.sex = 'N/A'
        self.faceURL = card['face']
        img_deal(self.faceURL,  '../static/cupFaces/'+str(self.uid)+'.png')
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

        return True

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

    def crawl_videoList(self):
        mpURL = f'https://api.bilibili.com/x/space/masterpiece?vmid={self.uid}&jsonp=jsonp'
        _json = requests.session().get(mpURL, headers=headers, timeout=5).json()
        data = _json['data']
        for v in data:
            self.masterPieces.append(self.extract_videoInfo1(v))
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
