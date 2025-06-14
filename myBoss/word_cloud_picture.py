import jieba  # 分词
from matplotlib import pylab as plt  # 绘图，数据可视化
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
from pymysql import connect
import json


def get_img(field, targetImgSrc, resImgSrc):
    con = connect(host='localhost', user='root', password='123456', database='bossInfo', port=3306, charset='utf8mb4')
    cursor = con.cursor()
    sql = f"select {field} from jobinfo"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for i in data:
        if i[0] != '无':
            companyTags = json.loads(i[0])[0].split('，')
            for j in companyTags:
                text += j
    cursor.close()
    con.close()
    data_cut = jieba.cut(text, cut_all=False)
    stop_words = []
    # with open('./stopwords.txt', 'r', encoding='utf8') as rf:
    #     for line in rf:
    #         if len(line) > 0:
    #             stop_words.append(line.strip())
    # data_result = [x for x in data_cut if x not in stop_words]
    string = ' '.join(data_cut)

    # 图片
    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure()
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImgSrc, dpi=800)


def get_img2(field, targetImgSrc, resImgSrc):
    con = connect(host='localhost', user='root', password='123123', database='bossinfo', port=3306, charset='utf8mb4')
    cursor = con.cursor()
    sql = f"select {field} from jobinfo"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for i in data:
        text += i[0]
        # if i[0] != '无':
        #     companyTags = json.loads(i[0])[0].split('，')
        #     for j in companyTags:
        #         text += j
    cursor.close()
    con.close()
    data_cut = jieba.cut(text, cut_all=False)
    stop_words = []
    with open('./stopwords.txt', 'r', encoding='utf8') as rf:
        for line in rf:
            if len(line) > 0:
                stop_words.append(line.strip())
    data_result = [x for x in data_cut if x not in stop_words]
    string = ' '.join(data_result)

    # 图片
    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure()
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImgSrc, dpi=800)

# get_img('companyTags', '../static/1.jpg', '../static/companyTags_cloud.jpg')
