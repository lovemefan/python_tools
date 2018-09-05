# coding: utf-8

import json

import jieba.analyse
import matplotlib as mpl
from scipy.misc import imread
from wordcloud import WordCloud

# mpl.use('TkAgg')
import matplotlib.pyplot as plt


def keywords(mblogs):
    text = []
    for blog in mblogs:
        keyword = jieba.analyse.extract_tags(blog['text'])
        text.extend(keyword)
    return text


def gen_img(texts, img_file):
    data = ' '.join(text for text in texts)
    image_coloring = imread(img_file)
    wc = WordCloud(
        background_color='white',
        mask=image_coloring,
        max_font_size=500,  # 设置字体最大值
        font_path='Fonts/HYC6GFM.TTF',
        random_state = 30  # 设置有多少种随机生成状态，即有多少种配色方案
    )
    wc.generate(data)
    # plt.figure()
    # plt.imshow(wc, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()

    wc.to_file(img_file.split('.')[0] + '_wc.png')


if __name__ == '__main__':
    keyword = 'shida'
    # 读取result_{}.json文件,取出词汇
    mblogs = json.loads(open('result_{}.json'.format(keyword), 'r', encoding='utf-8').read())
    print('微博总数：', len(mblogs))

    words = []
    for blog in mblogs:
        words.extend(jieba.analyse.extract_tags(blog['text']))

    print("总词数：", len(words))
    print(words)
    gen_img(words, '手印.jpg')
