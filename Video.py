import requests
from bs4 import BeautifulSoup
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd


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


if __name__ == "__main__":
    v = Video()
    v.bvid = 'BV15y4y177aj'
    #v.generate_wordscloud_1()
    #v.generate_wordscloud_2()

    v1 = Video()
    v1.bvid = 'BV1aK411P7hM'
    v1.generate_wordscloud_1()
    v1.generate_wordscloud_2()