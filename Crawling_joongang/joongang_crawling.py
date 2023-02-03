import sys
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import re

URL_BEFORE_KEYWORD = "https://www.joongang.co.kr/search/news?keyword="
URL_BEFORE_PAGE_NUM = "&page="

font_name = 'Malgun Gothic'



def get_link(key_word, page_range):
    link =[]

    for page in range(page_range):
        current_page = page + 1
        crawling_url_list = URL_BEFORE_KEYWORD + key_word + URL_BEFORE_PAGE_NUM + str(current_page)

        response = requests.get(crawling_url_list)
        soup = BeautifulSoup(response.text, 'lxml')
        url_tag = soup.select('ul.story_list > li.card >div.card_body > h2.headline > a ')

        for url in url_tag:
            link.append(url['href'])

    return link

def get_article(link):
    total_list = []

    for i in range(len(link)):
        url2 = link[i]
        response = requests.get(url2)
        soup = BeautifulSoup(response.text, 'lxml')
        t = str(soup.select('header.article_header > h1.headline'))
        t = re.sub('<.+?>','',t,0).strip()
        total_list.append(t.replace("\n",""))
        c = soup.select('div.article_body > p')
        total_list.append(c)

    return total_list

def wordcount(total_list):
    string = str(total_list)

    engine = Okt()

    all_nouns = engine.nouns(string)
    nouns = [n for n in all_nouns if len(n) > 1]

    global count, by_num

    count = Counter(nouns)
    by_num = OrderedDict(sorted(count.items(), key=lambda t:t[1], reverse=True))

    word = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    return word, number

def full_vis_bar(word, number):
    word20 = word[:20]
    number20 = number[:20]

    fig = plt.gcf()
    fig.set_size_inches(20, 10)
    matplotlib.rc('font', family=font_name, size=10)
    plt.title("전체 단어 빈도 수", fontsize=20)
    plt.xlabel('단어', fontsize=20)
    plt.ylabel('개수', fontsize=20)
    plt.bar(word20, number20, color='#6799FF')
    plt.xticks(rotation=90)
    plt.savefig('all_words.jpg')
    plt.show()

def main(argv):

    key_word = input(str("검색어를 입력하세요 : "))
    page_range = input(str("페이지를 입력하세요 : "))
    link = get_link(key_word, int(page_range))
    total_list = get_article(link)
    word, number = wordcount(total_list)
    full_vis_bar(word, number)

if __name__ == '__main__':
    main(sys.argv)