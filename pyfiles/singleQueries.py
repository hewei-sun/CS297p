from pyfiles.Video import Video
from pyfiles.Uploader import Uploader
from pyfiles.Spider import Spider
from pyfiles.MysqlConnect import MysqlConnect

def searchUp(input):
    uid, isPossibleTopUp = None, False

    # 1. get uid first
    if input.isdigit(): # search by ID
        uid = input
    else: # search by name/alias
        url = f'https://search.bilibili.com/upuser?keyword={input}'
        spider = Spider(url)
        spider.setSoup()
        link = spider.findTagByAttrs('li', {'class': 'user-item'})[0].find('a').get('href')
        uid = link[len('//space.bilibili.com/'):][:-len('?from=search')]

    # 2. see whether we have his/her individual table, this decides what we can return for his/her personal analysis page
    mysqlconnect = MysqlConnect()
    sql = f"SHOW TABLES LIKE 'Up{uid}';"
    tableExisted = mysqlconnect.queryOutCome(sql)
    if tableExisted:
        isPossibleTopUp = True


    up = Uploader(uid, isPossibleTopUp)
    # Then with this up, you can crawl basic, crawl masterpieces/history video list, and his/her tags,
    # Also, I added a new funtion `return4data()` in Uploader, it will return date, 4 data, rank(if this up is a top 100) columns
    # return的格式你可以根据你调用的需要改
    return up

if __name__ == "__main__":
    up = searchUp("大会员")
    up.crawl_basic()
    #up.crawl_videoList()
    print(up.__dict__)
    print(up.return4data())




