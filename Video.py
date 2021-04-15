import requests
from bokeh.io import webdriver
from bs4 import BeautifulSoup
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import json
import time, random
from pandas import Series, DataFrame
from Spider import Spider


class Video:
    def __init__(self, rank=None, title=None, bv=None, score=None, play=None, view=None, up_name=None, up_id=None):
        self.rank = rank
        self.title = title
        self.bvid = bv
        self.score = score
        self.play = play
        self.view = view
        self.up_name = up_name
        self.up_id = up_id

    def __str__(self):
        return '{}.\tTitle:{}\tBVID:{}\tPlay:{}\tView:{}\tAuthor:{}\tAuthourID:{}\n'.format(self.rank, self.title, self.bvid,
                                                                                          self.play, self.play,
                                                                                            self.up_name, self.up_id)

    def get_info(self):
        return [self.rank, self.title, self.bvid, self.score, self.play, self.view, self.up_name, self.up_id]

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

    def comments_parse(self):


        oid = self.get_oid(f'https://www.bilibili.com/video/{self.bvid}')
        n = 1
        headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/86.0.4240.75 Safari/537.36'}
        df = []
        try:
            while True:
                url = f'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={n}&type=1&oid={oid}&sort=2'
                print(url)
                r = requests.get(url.format(n), headers=headers)
                _json = json.loads(r.text)
                n += 1
                for replie in _json['data']['replies']:
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
                time.sleep(random.random())
        except:
            pass
        df = DataFrame(df)
        return df

if __name__ == "__main__":
    v = Video()
    v.bvid = 'BV15y4y177aj'
    #v.generate_wordscloud_1()
    #v.generate_wordscloud_2()
    v.comments_parse().to_csv('comments.csv')





