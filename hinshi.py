'''
英文を単語ごとに分かち書きし,
weblioからそれぞれの単語のレベルを取得(スクレイピング)した後に、
合計レベル / 単語数 で平均を求める
'''
import requests
from bs4 import BeautifulSoup

# 英文
content = 'Camber Pharmaceuticals, Inc. recalled 87 lots of the blood pressure \
        medication losartan on Thursday after discovering trace amounts of a \
        potential carcinogen. The recalled \
        25 mg, 50 mg and 100 mg tablets contained small amounts of N-Nitroso \
        N-Methyl 4-amino butyric acid, or NMBA, according to a company'

search_list = []
content = content.split(' ')

for w in content:
    if len(w) >= 4:                     # 単語が4文字以上かどうか
        if w[0] != w[0].upper():        # 単語の文頭が大文字かどうか(固有名詞は除く)
            if w.isalpha():             # 単語が数字かどうか(数字は除く)
                search_list.append(w)

# print(search_list)

tmp_url = 'https://ejje.weblio.jp/content/'
word_cnt = 0
level_sum = 0
for w in search_list:
    url = tmp_url + w
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")

    all_level = soup.find_all('span', class_='learning-level-content')

    if all_level:
        word_cnt += 1
        level = all_level[0].contents[0]
        level_sum += int(level)
        # print(level)

print(int(level_sum / word_cnt))
