from pyfiles.WEBvideo import Video
from pyfiles.WEBuploader import Uploader
from pyfiles.Spider import Spider
from pyfiles.MysqlConnect import MysqlConnect

def searchUp(input):
    # 1. get uid first
    # search by name/alias
    url = f'https://search.bilibili.com/upuser?keyword={input}'
    spider = Spider(url)
    spider.setSoup()
    link = spider.findTagByAttrs('li', {'class': 'user-item'})[0].find('a').get('href')
    uid = link[len('//space.bilibili.com/'):][:-len('?from=search')]
    return uid

def ifPossible(uid):
    # 2. see whether we have his/her individual table, this decides what we can return for his/her personal analysis page
    mysqlconnect = MysqlConnect()
    sql = f"SHOW TABLES LIKE 'Up{uid}';"
    tableExisted = mysqlconnect.queryOutCome(sql)
    if tableExisted:
        return True
    return  False

def searchVideo(input):
    if input.isdigit():  # search by ID
        bvid = input
    else:  # search by name/alias
        url = f'https://search.bilibili.com/video?keyword={input}'
        spider = Spider(url)
        spider.setSoup()
        link = spider.findTagByAttrs('li', {'class': 'video-item matrix'})[0].find('a').get('href')
        #print(link)
        bvid = link[len('//www.bilibili.com/video/'):][:-len('?from=search')]
        #print(bvid)
    v = Video(bvid)
    return v

if __name__ == "__main__":
    up = searchUp("大会员")
    up.crawl_basic()
    #up.crawl_videoList()
    print(up.__dict__)
    print(up.return4data())




