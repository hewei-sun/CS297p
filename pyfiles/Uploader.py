import time

from prepareTopUp import getLikesByID
from Video import Video
import requests
from Spider import Spider
from collections import Counter

user_agents='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
headers = {'user-agent': user_agents,
           'referer': ''}

class Uploader:
    def __init__(self, uid=None):
        self.uid = uid
        self.name = None
        self.sex = None
        self.faceURL = None
        self.birthday = None
        self.place = None
        self.numFollowers = None
        self.numFollowings = None
        self.sign = None
        self.level = None
        self.official = None
        self.numLikes = None
        self.numViews = None

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
        _json = requests.session().get(url, headers=headers, timeout=5).json()
        card = _json['data']['card']
        self.name = card['name']
        self.sex = card['sex']
        self.faceURL = card['face']
        self.birthday = card['birthday']
        self.place = card['place']
        self.numFollowers = card['fans']
        self.numFollowings = card['attention']
        self.sign = card['sign']

        self.level = card['level_info']['current_level']

        if card['Official']:
            self.official = card['Official']['title'] + '\n' + card['Official']['desc']

        self.numLikes, self.numViews = getLikesByID(self.uid)

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

if __name__ == "__main__":
    # https: // space.bilibili.com / 5970160
    #up = Uploader(5970160)
    up = Uploader(218869446)
    up.crawl_basic()
    up.crawl_videoList()
    print(up)





