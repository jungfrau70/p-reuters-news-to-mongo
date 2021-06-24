# 라이브러리 로드
# requests는 작은 웹브라우저로 웹사이트 내용을 가져온다.
import requests
# BeautifulSoup 을 통해 읽어 온 웹페이지를 파싱한다.
from bs4 import BeautifulSoup as bs
from datetime import datetime

# 크롤링 후 결과를 데이터프레임 형태로 보기 위해 불러온다.
import pandas as pd
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

url = 'https://www.reuters.com/news/archive/fainancenews?view=page&page=1&pageSize=10'

res = requests.get(url, headers=headers)
# print(res)
res.raise_for_status()

time.sleep(4)

soup = bs(res.text, 'html.parser')
# print(soup)
news_list = soup.find_all('div', attrs={'class': 'column1 col col-10'})

# print(len(news_list))
#
# for news in news_list:
titles = news_list[0].select('.story-content > a > h3')
contents = news_list[0].select('.story-content > p')
dates = news_list[0].select('.article-time')

re_titles = []; re_contents = []; re_dates = []
for title, content, date in zip(titles, contents, dates):
    # print(title.text.strip())
    re_titles.append(title.text.strip())
    # print(content.text.strip())
    re_contents.append(content.text.strip())
    # print(date.text.strip())
    re_dates.append(date.text.strip())

print(len(re_titles), len(re_contents), len(re_dates))
# for title, content, date in zip(re_titles, re_contents, re_dates):
#     print(title, '\n', content, '\n', date, '\n')

list_of_tuples = list(zip(re_titles, re_contents, re_dates))
df = pd.DataFrame(list_of_tuples, columns=['title', 'content', 'date'])
print(df)
# titles = soup.find_all('h3', attrs={'class': 'story-title'})
# dates = soup.find_all('span', attrs={'class': 'timestamp'})
# contents = soup.find_all('div', attrs={'class': 'story-content'})

# for content in contents:
#     print(content.find('p'))

# for p in contents.findall('p'):
#     print(p.text)

# for title in titles:
#     print(title.text)
#


# title = soup.select_one('#_siteviewTopArea > div.search_address > strong').text
# date = soup.select('#content > section:nth-child(3) > div > div.column1.col.col-10 > section > section > div')
# title = soup.select('//*[@id="content"]')
# soup.select('dev', {})

# print(title)