import sys
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt

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


def wordcount(file1, file2):
    f = open(file1, 'r', encoding='utf8')
    g = open(file2, 'w', encoding='utf8')

    engine = Okt()
    data = f.read()
    print(data)
    print(type(data))
    all_nouns = engine.nouns(data)
    # 길이가 1 이상인 것만 추출 (한글자짜리 제외)
    nouns = [n for n in all_nouns if len(n) > 1]

    global count, by_num

    count = Counter(nouns)
    by_num = OrderedDict(sorted(count.items(), key=lambda t: t[1], reverse=True))

    word = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    for w, n in zip(word, number):
        final1 = f"{w}  {n}"
        g.write(final1 + '\n')

    f.close(), g.close()


def full_vis_bar(by_num):
    for w, n in list(by_num.items()):
        if n <= 15:
            del by_num[w]

    fig = plt.gcf()
    fig.set_size_inches(20, 10)
    matplotlib.rc('font', family=font_name, size=10)
    plt.title("전체 단어 빈도 수", fontsize=20)
    plt.xlabel('단어', fontsize=20)
    plt.ylabel('개수', fontsize=20)
    plt.bar(by_num.keys(), by_num.values(), color='#6799FF')
    plt.xticks(rotation=90)
    plt.savefig('all_words.jpg')
    plt.show()

def top_n(file2, file3):
    # 교안과 다르게 처리를 하는데 wordcount.txt를 읽어서 10개를 추출한 다음, file3(top.txt)로 저장하는 코드 작성
    f = open(file2, 'r', encoding='utf8')
    g = open(file3, 'w', encoding='utf8')

    test = f.readlines()
    test_list = test[:10]
    refine_list = []

    for i in test_list:
        refine_list.append(i.replace("\n", ""))

    g.write('\n'.join(refine_list))
    f.close(), g.close()

def main(argv):
    if len(argv) != 3:
        print("인자 값을 정확히 입력하세요")
        return

    file1 = "crawling.txt"
    file2 = "wordcount.txt"
    file3 = "top.txt"
    # argv[0]은 파일 명을 의미
    key_word = argv[1]
    page_range = int(argv[2])
    link = get_link(key_word, page_range)
    get_article(file1, link, key_word, page_range)
    wordcount(file1, file2)
    full_vis_bar(by_num)
    top_n(file2, file3)

if __name__ == '__main__':
    main(sys.argv)