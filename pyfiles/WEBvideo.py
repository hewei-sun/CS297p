import requests
from bs4 import BeautifulSoup
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import json
import time, random
from pandas import Series, DataFrame
from pyfiles.Spider import Spider
from pyfiles.WEBconvert import cover_deal

user_agents='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
headers = {'user-agent': user_agents,
           'referer': ''}


class Video:
    def __init__(self, bvid=None):
        self.rank = None
        self.title = None
        self.bvid = bvid
        #self.score = None
        self.play = None
        self.view = None # danmu
        self.up_name = None
        self.up_id = None
        self.cover_url = None

        # below attributes will be collected from ways other than ranking crawling
        self.description = None
        self.tname = None # Some video has been stated its primary tag name
        self.publish_time = None
        self.duration = None
        self.reply = None #评论
        self.like = None #点赞
        self.coin = None #币
        self.collect = None #收藏
        self.share = None #转发
        self.tags = []  # ordered by weight, more left more weighted.

    def __str__(self):
        return '{}.\tTitle:{}\tBVID:{}\tPlay:{}\tView:{}\t' \
               'Author:{}\tAuthourID:{}\tCoverURL:{}\n'.format(self.rank, self.title, self.bvid,self.play, self.view, self.up_name, self.up_id,self.cover_url)
    def printInfo(self):
        for key,val in self.__dict__.items():
            if val: print(key,' : ',val)

    def get_cover(self):
        url = f'https://www.bilibili.com/video/{self.bvid}'
        spider = Spider(url, headers)
        spider.setSoup()
        '''
        if spider.soup.find('div', {'id': 'app', 'class': 'main-container clearfix'}):
            self.cover_url = spider.soup.find('meta', {'property': 'og:image'}).get('content')
            return
        '''
        cover_url = spider.soup.find('meta', {'property': 'og:image'})
        if cover_url:
            cover_url = cover_url.get('content')
        else:
            cover_url = spider.soup.find('meta', {'itemprop': 'image'})
            cover_url = cover_url.get('content') if cover_url else None
        cover_deal(cover_url, '/static/videoFaces/' + self.bvid + '.png')
        return cover_url

    def start_crawlling(self, for_rank=False):
        if not self.bvid:
            print("No BVid Given Yet.")
            return
        if self.bvid[0:2] != 'BV':  # 官方番剧/动画
            url = f'https://www.bilibili.com/bangumi/play/{self.bvid}'
            print(url)
            headers['referer'] = url
            spider = Spider(url, headers)
            spider.setSoup()
            self.title = spider.soup.find('title').text
            if not for_rank: self.description = spider.soup.find('meta', {'name':'description'}).get('content')
            self.up_name = spider.soup.find('meta', {'name':'author'}).get('content')
            self.cover_url = spider.soup.find('meta', {'property':'og:image'}).get('content')
            return

        url = f'https://www.bilibili.com/video/{self.bvid}'
        print(url)
        headers['referer'] = url
        spider = Spider(url, headers)
        spider.setSoup()

        if spider.soup.find('div', {'id':'app', 'class':'main-container clearfix'}):
            self.title = spider.soup.find('title').text
            if not for_rank: self.description = spider.soup.find('meta', {'name': 'description'}).get('content')
            self.up_name = spider.soup.find('meta', {'name': 'author'}).get('content')
            self.cover_url = spider.soup.find('meta', {'property': 'og:image'}).get('content')
            return

        self.description = spider.soup.find('meta',{'itemprop':'description'}).get('content')
        statistics = spider.soup.find('div',{'id':'viewbox_report'}).find_all('span')
        self.title = statistics[0].text
        self.play = statistics[1].text[:-5]
        self.view = statistics[2].text[:-2]
        if not for_rank: self.publish_time = statistics[3].text
        if len(statistics)>4 and not for_rank: # the video has a history rank
            self.rank = statistics[4].text.strip()
        # 独立作者 or 协作团队
        single_up = spider.soup.find('div',{'class':'up-info_right'})
        if single_up:
            up = single_up.find('a',{'class':'username'})
            self.up_id = up.get('href')[len('//space.bilibili.com/'):]
            self.up_name = up.text.strip()
        else:
            team = spider.soup.find('div',{'class':'members-info__container'})
            if team:
                up = team.find_all('div',{'class':'avatar-name__container'})[0].find('a')
                self.up_id = up.get('href')[len('//space.bilibili.com/'):]
                self.up_name = up.text.strip()

        self.cover_url = spider.soup.find('meta', {'itemprop': 'image'}).get('content')

        if not for_rank:
            self.like = spider.soup.find('span',{'class':'like'}).text.strip()  # 点赞
            self.coin = spider.soup.find('span',{'class':'coin'}).text.strip()  # 币
            self.collect = spider.soup.find('span',{'class':'collect'}).text.strip()  # 收藏
            self.share = spider.soup.find('span',{'class':'share'}).text.strip()  # 转发
            for item in spider.soup.find_all('li', {'class':'tag'}):
                self.tags.append(item.text.strip())

    def get_cid(self):
        url = 'https://api.bilibili.com/x/web-interface/view?bvid={}'.format(self.bvid)
        response = requests.get(url).text
        pattern = "(\"cid\"\:)(\d+)"
        match = re.findall(pattern,response)
        return match[0][1]

    def collect_danmuku(self):
        # collect all live screen and save them into a dataframe
        cid = self.get_cid()
        url = f'https://comment.bilibili.com/{cid}.xml'
        #print(url)
        request = requests.get(url)
        request.encoding='utf8'
        soup = BeautifulSoup(request.text, 'lxml')
        danmuku = [i.text for i in soup.find_all('d')]
        return danmuku

    def segment_danmuku(self):
        # get rid of digits, spaces, invalid words
        danmuku = self.collect_danmuku()
        print('# OF Danmuku:', len(danmuku))
        segment_words = []
        for danmu in danmuku:
            try:
                words = jieba.cut(danmu) # cut danmu into words
                words = [w for w in words if not str(w).isdigit()]
                words = list(filter(lambda x: x.strip(), words))
                for w in words:
                    if len(w)>1 and w!='\r\n':
                        segment_words.append(w)
            except:
                print(danmu)
                continue
        words_df = pd.DataFrame({'segment':segment_words})
        words_df = words_df.groupby(['segment']).segment.count()
        words_df = words_df.sort_values(ascending=False).reset_index(name='frequency')
        frequency_table = {x[0]:x[1] for x in words_df[:500].values}
        return frequency_table

    def generate_wordscloud_1(self):
        # generate for all words
        frequency = self.segment_danmuku()
        background_image = plt.imread('background.jpg')
        wc = WordCloud(
            background_color='black',
            font_path='font/chinese.simhei.ttf',
            #stopwords=STOPWORDS,
            mask=background_image,
            max_words=10000,
            max_font_size=500,
            random_state=30)
        wc.generate_from_frequencies(frequency)
        image_colors = ImageColorGenerator(background_image)
        wc.recolor(color_func=image_colors)
        plt.figure(figsize=(15, 10))
        plt.imshow(wc)
        plt.axis('off')
        plt.show()

    def generate_wordscloud_2(self):
        # generate words cloud for only adjective words
        import jieba.posseg as psg
        danmuku = self.collect_danmuku()
        words_list = []
        for danmu in danmuku:
            words = psg.cut(danmu)
            for w in words:
                words_list.append((w.word, w.flag))
        words_list = pd.DataFrame(words_list, columns=['word','type'])
        words_list = words_list.groupby(['type','word']).word.count()
        words_list = words_list.reset_index(name='count')
        df_a_count = words_list[words_list['type'].isin(['a'])].sort_values(by='count', ascending=False)
        tag_list = {i[1]: i[2] for i in df_a_count.values}
        background_image = plt.imread('background.jpg')
        wc = WordCloud(
            background_color='black',
            font_path='font/chinese.simhei.ttf',
            # stopwords=STOPWORDS,
            mask=background_image,
            max_words=10000,
            max_font_size=500,
            random_state=30)
        wc.generate_from_frequencies(tag_list)
        image_colors = ImageColorGenerator(background_image)
        wc.recolor(color_func=image_colors)
        plt.figure(figsize=(14, 8))
        plt.imshow(wc)
        plt.axis('off')
        plt.show()

    def get_oid(self, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        r = requests.get(url, headers=headers)
        res = r.text
        patten = '<meta data-vue-meta="true" itemprop="url" content="https://www.bilibili.com/video/av(.*?)/">'
        oid = re.findall(patten, res)
        aim_oid = oid[0]
        patten1 = '<meta data-vue-meta="true" property="og:title" content="(.*?)">'
        video_title = re.findall(patten1, res)
        if video_title:
            self.video_title = video_title[0].split('_哔哩哔哩')[0]
        return aim_oid

    def comments_parse(self, hot_num = None, max=None):
        oid = self.get_oid(f'https://www.bilibili.com/video/{self.bvid}')
        n = 1
        i = 0
        headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/86.0.4240.75 Safari/537.36'}
        df = []
        try:
            while i<max:
                if max and i>=max: break
                url = f'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={n}&type=1&oid={oid}&sort=2'
                print('Visiting comment page: ',url)
                r = requests.get(url.format(n), headers=headers, timeout=5)
                _json = json.loads(r.text)
                n += 1
                for replie in _json['data']['replies']:
                    i += 1
                    item = {}
                    item['user_id'] = replie.get('member').get('mid')  # 用户id
                    item['user_name'] = replie.get('member').get('uname')  # 用户名
                    item['user_sex'] = replie.get('member').get('sex')  # 性别
                    item['user_level'] = replie.get('member').get('level_info').get('current_level')  # 等级
                    vip = replie.get('member').get('vip').get('vipStatus')  # 是否vip
                    if vip == 1:
                        item['user_is_vip'] = 'Y'
                    elif vip == 0:
                        item['user_is_vip'] = 'N'
                    comment_date = replie.get('ctime')  # 评论日期
                    timeArray = time.localtime(comment_date)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    item['apprecate_count'] = replie.get('like')  # 点赞数
                    item['reply_count'] = replie.get('rcount')  # 回复数
                    item['comment_date'] = otherStyleTime
                    item['comment'] = replie.get('content').get('message')  # 评论内容
                    df.append(item)
                    if max and i>=max:
                        break
                else:  # Continue if the inner loop wasn't broken.
                    time.sleep(random.random()*2)
                    continue
                # Inner loop was broken, break the outer.
                break

        except:
            pass

        df = DataFrame(df)
        return df

if __name__ == "__main__":
    v = Video()
    v.bvid = 'BV1V5411u7yy'
    v.start_crawlling()
    v.printInfo()
    #v.comments_parse(50).to_csv('comments.csv')
    v.generate_wordscloud_1()
    v.generate_wordscloud_2()
