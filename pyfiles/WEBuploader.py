import time
import requests
from pyfiles.WEBvideo import Video
from pyfiles.Spider import Spider
from collections import Counter
import random
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
        #print(_json['message'])
        if not _json['data']:
            return
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
            
    def __repr__(self):
        return repr((self.uid, self.name, self.sex, self.faceURL, self.birthday, self.place, self.numFollowings, self.numFollowers,self.sign,self.level,self.numViews,self.numLikes))

if __name__ == "__main__":
    # https: // space.bilibili.com / 5970160
    #up = Uploader(5970160)
    up = Uploader(218869446)
    up.crawl_basic()
    up.crawl_videoList()
    print(up)





