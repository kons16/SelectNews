'''
ニュース記事をスクレイピングして内容を取得, レベルを表示する
'''
import requests
from bs4 import BeautifulSoup
from bs4 import element

top_url = 'https://www.usatoday.com/news/'      # ニュース記事を取得するURL
stroy_url = 'https://www.usatoday.com'          # ニュース記事の元となるURL
tmp_url = 'https://ejje.weblio.jp/content/'     # 単語のレベルを調べる元となるURL

# topに記載されているニュース記事のURLを取得
html = requests.get(top_url).content
soup = BeautifulSoup(html, "html.parser")

top_content = soup.find_all('p', itemprop='headline')
title_url = soup.find_all('a', itemprop='url')

'''
for t in title:
    print(t.contents[0])
'''

url_content = {}    # 記事のURL:記事内容 で格納
title_level = {}    # 記事のタイトル:レベル で格納
link_url = []       # ニュース記事のURL
# 記事のURLを取得する
for t in title_url:
    split_url = t.get('href').split('/')
    if split_url[1] == 'story':
        link_url.append(stroy_url + t.get('href'))


news_title = []
# link先の記事内容を取得し, 辞書に代入
for link in link_url:
    html2 = requests.get(link).content
    soup2 = BeautifulSoup(html2, "html.parser")

    if soup2.find('p', class_='speakable-p-1 p-text'):
        t1 = soup2.find('p', class_='speakable-p-1 p-text').contents[0]
        t2 = soup2.find('p', class_='speakable-p-2 p-text').contents[0]
        # 文がTag型でなかったとき辞書に格納する, そのURLのタイトルを保存
        if type(t1) != element.Tag and type(t2) != element.Tag:
            # ニュース記事のタイトルを取得
            title = soup2.find('h4', class_='util-bar-share-summary-title')
            news_title.append(title.contents[0])
            url_content[link] = t1 + t2


# k-URL v-content
for k, t in zip(url_content.keys(), news_title):
    search_list = []    # レベルを調べる単語
    word_cnt = 0        # 単語数
    level_sum = 0       # 単語の合計レベル

    content = url_content[k].split(' ')

    for w in content:
        if len(w) >= 4:                     # 単語が4文字以上かどうか
            if w[0] != w[0].upper():        # 単語の文頭が大文字かどうか(固有名詞は除く)
                if w.isalpha():             # 単語が数字かどうか(数字は除く)
                    search_list.append(w)

    # print(search_list)

    for w in search_list:
        url = tmp_url + w
        html3 = requests.get(url).content
        soup3 = BeautifulSoup(html3, "html.parser")

        all_level = soup3.find_all('span', class_='learning-level-content')

        if all_level:
            word_cnt += 1
            level = int(all_level[0].contents[0])    # 単語単体のレベル
            level_sum += int(level)

    avg_level = int(level_sum / word_cnt)
    title_level[t] = str(avg_level)
    print(t + " " + "レベル:" + str(avg_level))
    print(k)
    print()
