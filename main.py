'''
ニュース記事をAPIで取得してレベル評価する
'''
from flask import Flask, request, abort, render_template
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import json
from bs4 import BeautifulSoup, element

app = Flask(__name__)

top_url = 'https://www.usatoday.com/news/'      # ニュース記事を取得するURL
stroy_url = 'https://www.usatoday.com'          # ニュース記事の元となるURL
tmp_url = 'https://ejje.weblio.jp/content/'     # 単語のレベルを調べる元となるURL

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
API_KEY = os.getenv('API_KEY')
api = 'https://newsapi.org/v2/top-headlines?sources=cnn&apiKey={key}'
api2 = 'https://newsapi.org/v2/top-headlines?sources=usa-today&apiKey={key}'


@app.route('/')
def index():
    return render_template('index.html')


# CNNから取得
@app.route('/get_level', methods=['POST'])
def get_level():
    url_list = []       # 記事のURLを格納
    title_level = {}    # 記事のタイトル:レベル で格納
    news_title = []
    avg_list = []
    url = api.format(key=API_KEY)
    r = requests.get(url)
    data = json.loads(r.text)
    articles = data['articles']

    for a in articles:
        if type(a['content']) == str:
            s = a['description'] + a['content']
        else:
            s = a['description']

        search_list = []    # レベルを調べる単語
        word_cnt = 0        # 単語数
        level_sum = 0       # 単語の合計レベル

        content = s.split(' ')

        for w in content:
            if len(w) >= 4:                     # 単語が4文字以上かどうか
                if w[0] != w[0].upper():        # 単語の文頭が大文字かどうか(固有名詞は除く)
                    if w.isalpha():             # 単語が数字かどうか(数字は除く)
                        search_list.append(w)

        for w in search_list:
            url = tmp_url + w
            html = requests.get(url).content
            soup = BeautifulSoup(html, "html.parser")

            all_level = soup.find_all('span',
                                      class_='learning-level-content')

            if all_level:
                word_cnt += 1
                level = int(all_level[0].contents[0])    # 単語単体のレベル
                level_sum += int(level)

        avg_level = int(level_sum / word_cnt)

        avg_list.append(avg_level)
        news_title.append(a['title'])
        url_list.append(a['url'])

    return render_template('index.html', data=zip(news_title,
                           avg_list, url_list))


# USA TODAYから取得
@app.route('/get_today_level', methods=['POST'])
def get_today_level():
    url_list = []       # 記事のURLを格納
    title_level = {}    # 記事のタイトル:レベル で格納
    news_title = []
    avg_list = []
    s = ''              # 記事内容
    url2 = api2.format(key=API_KEY)
    r = requests.get(url2)
    data = json.loads(r.text)
    articles = data['articles']

    for a in articles:
        news_title.append(a['title'])
        url_list.append(a['url'])

        html = requests.get(a['url']).content
        soup = BeautifulSoup(html, "html.parser")

        if soup.find('p', class_='speakable-p-1 p-text'):
            t1 = soup.find('p', class_='speakable-p-1 p-text').contents[0]
            t2 = soup.find('p', class_='speakable-p-2 p-text').contents[0]
            # 文がTag型でなかったとき辞書に格納する, そのURLのタイトルを保存
            if type(t1) != element.Tag and type(t2) != element.Tag:
                s = t1 + t2

        search_list = []    # レベルを調べる単語
        word_cnt = 0        # 単語数
        level_sum = 0       # 単語の合計レベル

        content = s.split(' ')

        for w in content:
            if len(w) >= 4:                     # 単語が4文字以上かどうか
                if w[0] != w[0].upper():        # 単語の文頭が大文字かどうか(固有名詞は除く)
                    if w.isalpha():             # 単語が数字かどうか(数字は除く)
                        search_list.append(w)

        for w in search_list:
            url = tmp_url + w
            html = requests.get(url).content
            soup = BeautifulSoup(html, "html.parser")

            all_level = soup.find_all('span',
                                      class_='learning-level-content')

            if all_level:
                word_cnt += 1
                level = int(all_level[0].contents[0])    # 単語単体のレベル
                level_sum += int(level)

        avg_level = int(level_sum / word_cnt)
        avg_list.append(avg_level)

    return render_template('index.html', data=zip(news_title,
                           avg_list, url_list))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
