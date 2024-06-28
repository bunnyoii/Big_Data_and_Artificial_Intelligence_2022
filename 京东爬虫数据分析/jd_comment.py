# -*- endoding: utf-8 -*-
import requests  # 用于发送网络请求
import re  # 正则表达式库，用于文本匹配
from wordcloud import WordCloud  # 生成词云
import matplotlib.pyplot as plt  # 绘图库
from snownlp import SnowNLP  # 中文文本情感分析库

'''
https://club.jd.com/comment/productPageComments.action?
callback=fetchJSON_comment98
&productId=1233203
&score=0
&sortType=5
&page=1
&pageSize=10
&isShadowSku=0
&fold=1
'''


def fetch_comments():
    comments = []  # 存储提取的评论
    first = 1  # 评论序号，用于打印
    for i in range(1, 50):  # 循环50页评论
        # 构建请求URL
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=1233203&score=0&sortType=5&pageSize=10&isShadowSku=0&fold=1&page='
        finalurl = url + str(i)

        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        }  # 请求头部，模仿浏览器行为
        data = requests.get(url=finalurl, headers=header).text
        remodel_comment = re.compile(r'\"content\":\"([^"]+)\",\"(?:creationTime|vcontent)\"')  # 正则表达式匹配评论内容
        comment_list = remodel_comment.findall(data)

        for comment in comment_list:
            print(first, ":", comment)
            first += 1
            comments.append(comment)  # 将评论添加到列表中
    return comments

def analyze_sentiments(comments):
    sentiments = []  # 存储情感分析结果
    for comment in comments:
        s = SnowNLP(comment)  # 使用SnowNLP进行情感分析
        sentiments.append(s.sentiments)
    positive_count = sum(1 for x in sentiments if x > 0.6)  # 计算积极评论数
    neutral_count = sum(1 for x in sentiments if 0.4 <= x <= 0.6)  # 计算中性评论数
    negative_count = sum(1 for x in sentiments if x < 0.4)  # 计算消极评论数
    return [positive_count, neutral_count, negative_count]

def create_sentiment_pie_chart(sizes):
    labels = ['Positive', 'Neutral', 'Negative']
    colors = ['#599e5e', '#3c78a9', '#c84f4f']
    explode = (0.1, 0, 0)  # 突出显示积极部分
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Comment Sentiment Distribution')
    plt.axis('equal')
    plt.show()

def create_wordcloud(comments):
    text = " ".join(comments)  # 将所有评论合并为一个长字符串
    font_path = 'C:/Windows/Fonts/simhei.ttf'
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def main():
    comments = fetch_comments()
    sentiment_counts = analyze_sentiments(comments)
    create_sentiment_pie_chart(sentiment_counts)
    create_wordcloud(comments)

if __name__ == '__main__':
    main()