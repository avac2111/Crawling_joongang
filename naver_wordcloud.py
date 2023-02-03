import sys
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud

URL_BEFORE_KEYWORD = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
URL_BEFORE_PAGE_NUM = "&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=29&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start="

font_name = 'Malgun Gothic' # Mac은 Apple Gothic

def get_link(key_word, page_range):
    link=[] # 뉴스기사 제목

    for page in range(page_range):
        current_page= 1 + page*10
        crawling_url_list = URL_BEFORE_KEYWORD + key_word + URL_BEFORE_PAGE_NUM + str(current_page) # int->str 형변환

        # URL에 get 요청 보냄
        response = requests.get(crawling_url_list)
        soup = BeautifulSoup(response.text, 'lxml')
        url_tag = soup.select('div.news_area > a')

        for url in url_tag:
            link.append(url['href'])

    return link

def get_article(file1, link, key_word, page_range):
    with open(file1, 'w', encoding='utf-8') as f:
        i = 1

        for url2 in link:
            article = Article(url2, language='ko')

            try:
                article.download()
                article.parse()
            except:
                print(str(i) + '번째 url을 크롤링 할 수 없습니다')
                # print(f"{i}번 째 url을 크롤링 할 수 없습니다.")
                # print("{}번 째 url을 크롤링 할 수 없습니다.".format(i))
                continue

            news_title = article.title
            news_content = article.text

            f.write(news_title)
            f.write(news_content)

            i += 1
    f.close()

def wordcloud(filename):
    with open(filename, encoding='utf8') as f:
        data = f.read()

        engine = Okt()
        all_nouns = engine.nouns(data)

        nouns = [n for n in all_nouns if len(n) > 1]
        count = Counter(nouns)

        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', background_color=(168,237,244),
                       width=2500, height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))

        plt.imshow(cloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('cloud.jpg')
        plt.show()

def main(argv):
    if len(argv) != 3:
        print("인자값이 부족하거나 많습니다")
    else:
        filename = 'crawling_wc.txt'
        key_word = argv[1]
        page_range = int(argv[2])

        link = get_link(key_word, page_range)
        get_article(filename, link, key_word, page_range)
        wordcloud(filename)

if __name__ == '__main__':
    main(sys.argv)