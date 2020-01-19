from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + word
    return url

def select_first(driver):
    first = driver.find_element_by_css_selector('div._9AhH0')
    first.click()
    time.sleep(3)

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    try:
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ' '

    tags = re.findall(r'#[^\s#,\\]+', content)

    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]

    try:
        like = soup.select('div.Nm9Fw > button')[0].text[4:-1]
    except:
        like = 0
    
    try:
        place = soup.select('div.M30cS')[0].text
    except:
        place = ''

    data = [content, date, like, place, tags]
    return data

def move_next(drvier):
    right = driver.find_element_by_css_selector('a.HBoOv.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(1)

words = ['광주여행', '광주카페', '나주카페', '나주관광', '광주관광']
for word in words:
    driver = webdriver.Chrome('D:/DataAnalysis/chromedriver.exe')

    # word = '광주맛집'
    url = insta_searching(word)

    driver.get(url)
    time.sleep(3)

    select_first(driver)

    result = [ ]

    target = 150
    for i in range(target):
        data = get_content(driver)
        result.append(data)
        move_next(driver)

    print(len(result))
    print(result[:2])

    import pandas as pd

    results_df = pd.DataFrame(result)
    results_df.columns = ['content', 'date', 'like', 'place', 'tags']
    results_df.drop_duplicates(subset=['content'], inplace=True)
    results_df.to_excel('./files/{}.xlsx'.format(word), index=False)

insta_df = pd.DataFrame([])
folder = './files/'
f_list = ['광주여행.xlsx', '광주맛집.xlsx', '나주여행.xlsx', '나주맛집.xlsx']
for fname in f_list:
    fpath = folder + fname
    temp = pd.read_excel(fpath)
    insta_df = insta_df.append(temp)

insta_df.drop_duplicates(subset=['content'], inplace=True)
insta_df.to_excel('./files/광주나주맛집.xlsx', index=False)

raw_total = pd.read_excel('./files/광주나주맛집.xlsx')
raw_total['tags'][:3]

tags_total = []

for tags in raw_total['tags']:
    tags_list = tags[2:-2].split("', '")
    for tag in tags_list:
        tags_total.append(tag)

from collections import Counter
tag_counts = Counter(tags_total)

tag_counts.most_common(50)

STOPWORDS = ['', '#일상', '#맞팔', '#소통', '#좋아요'\
            , '#좋반', '#광주스팀세차', '#광주세차'\
            , '#광주손세차', '#나주출장세차', '#나주세차'\
            , '#나주손세차', '#나주한전']

tag_total_selected = []
for tag in tags_total:
    if tag not in STOPWORDS:
        tag_total_selected.append(tag)

tag_counts_selected = Counter(tag_total_selected)
tag_counts_selected.most_common(50)

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import sys

if sys.platform in ['win32', 'win64']:
    font_name = 'malgun gothic'
elif sys.platform == 'darwin':
    font_name = "AppleGothic"

rc('font', family=font_name)

tag_counts_df = pd.DataFrame(tag_counts_selected.most_common(30))
tag_counts_df.columns = ['tags', 'counts']

plt.figure(figsize = (10, 8))
sns.barplot(x = 'counts', y = 'tags', data = tag_counts_df)

from wordcloud import WordCloud
import platform

font_path = 'c:/Windows/Fonts/malgun.ttf'
wordcloud = WordCloud(font_path=font_path,
                    background_color='white',
                    max_words=100,
                    relative_scaling=0.3,
                    width=800,
                    height=400
                    ).generate_from_frequencies(tag_counts_selected)
plt.figure(figsize= (15, 10))
plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('./files/wordcloud.png')