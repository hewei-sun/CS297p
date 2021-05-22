from pyfiles.WEBVideo import Video
from pyfiles.Spider import Spider
from pyfiles.MysqlConnect import MysqlConnect
import time, random
import re

user_agents='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
headers = {'user-agent': user_agents,
           'referer': 'https://www.bilibili.com/'}

def delEmojis(text): # delete emojis in the given text, used for title of video
    emoji_pattern = re.compile("["
           u"\U0001F600-\U0001F64F"
           u"\U0001F300-\U0001F5FF"
           u"\U0001F680-\U0001F6FF"
           u"\U0001F1E0-\U0001F1FF"
           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', text)

def getRanking(field, url):  # Crawl a single ranking page
    spider = Spider(url,headers)
    spider.setSoup()
    itemList = spider.findTagByAttrs('li', {'class':'rank-item'})
    for itm in itemList:
        v = Video()
        v.bvid = itm.find('a', {'class': 'title'}).get('href')[len('//www.bilibili.com/video/'):]
        v.rank = int(itm.find('div', {'class': 'num'}).text)
        #v.start_crawlling(True) # true for telling crawller to only crawl needed info for present video in rankings

        v.title = delEmojis(itm.find('a', {'class': 'title'}).text)
        v.score = itm.find('div', {'class': 'pts'}).find('div').text
        dataBox = itm.find('div', {'class': 'detail'}).find_all('span')
        v.play = dataBox[0].text.strip()  # 播放量
        v.view = dataBox[1].text.strip()  # 弹幕
        v.up_name = dataBox[2].text.strip()
        v.up_id = itm.find('div', {'class': 'detail'}).find('a').get('href')[len('//space.bilibili.com/'):]
        v.cover_url = v.get_cover()
        insertToTable(field, v.rank, v.title, v.bvid, v.play, v.view, v.up_name, v.up_id, v.cover_url)

        time.sleep(random.random() * 5)


def getURLFormBilibili():
    rankingFields = {
        'all': '全站',
        #'bangumi': '番剧',
        #'guochan': '国产动画',
        'guochuang': '国创相关',
        #'documentary': '纪录片',
        'douga':'动画',
        'music':'音乐',
        'dance':'舞蹈',
        'game':'游戏',
        'technology':'知识',
        'digital':'数码',
        'car':'汽车',
        'life':'生活',
        'food':'美食',
        'animal':'动物圈',
        'kichiku':'鬼畜',
        'fashion':'时尚',
        'ent':'娱乐',
        'cinephile':'影视',
        #'movie':'电影',
        #'tv':'电视剧',
        'origin':'原创',
        'rookie':'新人'
    }
    urlDict = {}
    for field in rankingFields.keys():
        destinationURL = 'https://www.bilibili.com/v/popular/rank/{}'.format(field)
        urlDict[field] = destinationURL
    return urlDict

def prepareAllRankings():
    urlDict = getURLFormBilibili()
    for field, url in urlDict.items():
        prepareOneRanking(field, url)

def creatTable(field):
    mysqlconnect = MysqlConnect()
    sql = f"DROP TABLE IF EXISTS `RANK{field}`;"
    mysqlconnect.queryOutCome(sql)
    sql = f'''CREATE TABLE `RANK{field}`
            (
                `Rank` INT UNIQUE,
                `Title` VARCHAR(200),
                `BVid` VARCHAR(50) UNIQUE, 
                `Play` VARCHAR(50),
                `View` VARCHAR(50),
                `Up` VARCHAR(50),
                `Up_ID` INT,
                `Cover_URL` VARCHAR(200),
                 PRIMARY KEY(BVid)
            )ENGINE=innodb DEFAULT CHARSET=utf8;'''
    mysqlconnect.queryOutCome(sql)


def insertToTable(field, rank, title, bvid, play, view, up_name, up_id, cover_url):
    title = delEmojis(title)
    temp = [("'",r"\'"),('"',r'\"')]
    for old, new in temp:
        title = title.replace(old, new)
        up_name = up_name.replace(old, new)
    sql = '''
            INSERT IGNORE INTO `RANK{}` VALUES ({}, \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');
          '''.format(field, rank, title, bvid, play, view, up_name, up_id, cover_url)
    print(sql)
    mysqlconnect = MysqlConnect()
    mysqlconnect.queryOutCome(sql)
    return

def prepareOneRanking(field, url):
    print("Processing `",field,"` Ranking... at ",url)
    creatTable(field)
    getRanking(field, url)


def printRankings(rank):
    str = ''
    for v in rank:
        str += v.__str__()
    print(str)
    return str

if __name__ == "__main__":
    #prepareAllRankings()
    #fields = ['all', 'guochuang', 'douga', 'music', 'dance', 'game', 'technology', 'digital', 'car', 'life', 'food', 'animal',
              #'kichiku', 'fashion', 'ent', 'cinephile', 'origin', 'rookie']
    getRanking('all', 'https://www.bilibili.com/v/popular/rank/all')
