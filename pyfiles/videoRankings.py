from Video import Video
from Spider import Spider
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

def getRanking(url):  # Crawl a single ranking page
    spider = Spider(url,headers)
    spider.setSoup()
    itemList = spider.findTagByAttrs('li', {'class':'rank-item'})
    videosList = []
    for itm in itemList:
        rank = itm.find('div', {'class': 'num'}).text
        v = Video()
        v.bvid = itm.find('a', {'class': 'title'}).get('href')[len('//www.bilibili.com/video/'):]
        v.rank = rank
        v.start_crawlling()
        v.get_cover()
        '''
        v.title = delEmojis(itm.find('a', {'class': 'title'}).text)
        v.score = itm.find('div', {'class': 'pts'}).find('div').text
        dataBox = itm.find('div', {'class': 'detail'}).find_all('span')
        v.play = dataBox[0].text.strip()  # 播放量
        v.view = dataBox[1].text.strip()  # 弹幕
        v.up_name = dataBox[2].text.strip()
        v.up_id = itm.find('div', {'class': 'detail'}).find('a').get('href')[len('//space.bilibili.com/'):]
        '''
        videosList.append(v)
    return videosList

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
    rankings = {}
    urlDict = getURLFormBilibili()
    for field, url in urlDict.items():
        print("Processing `" + field + "` Ranking...")
        rankings[field] = getRanking(url)
        printRankings(rankings[field])
    return rankings

def prepareOneRanking(field):
    print("Processing `" + field + "` Ranking...")
    url = 'https://www.bilibili.com/v/popular/rank/{}'.format(field)
    print(url)
    ret = getRanking(url)
    printRankings(ret)
    return ret


def printRankings(rank):
    str = ''
    for v in rank:
        str += v.__str__()
    print(str)
    return str

if __name__ == "__main__":
    #rankings = prepareAllRankings()
    rank = prepareOneRanking('guochuang')
    '''
    for key, rank in rankings.items():
        print("Recent Trend of TOP1 video in " + key)
        v = rank[0]
        v.generate_wordscloud_1()
        v.generate_wordscloud_2()
    '''

    '''
    # 原先写进mysql的code如下,感觉用不到，就comment掉了。
    urlDict = getURLFormBilibili()
    mysqlconnect = MysqlConnect()

    for field, url in urlDict.items():
        print("Processing `" + field + "` Ranking...")
        createsql = mysqlconnect.getCreateTableSql(field)
        mysqlconnect.createTable(field, createsql)
        videosList = getRanking(url)
        for video in videosList:
            info = video.get_info()
            # print(info)
            insertsql = mysqlconnect.getInsertToTableSql(field, info[0], info[1], info[2], info[3], info[4],
                                                         info[5], info[6], info[7])
            mysqlconnect.insertInfo(insertsql)
    '''