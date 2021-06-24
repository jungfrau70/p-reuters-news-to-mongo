# 라이브러리 로드
# requests는 작은 웹브라우저로 웹사이트 내용을 가져온다.
import requests
# BeautifulSoup 을 통해 읽어 온 웹페이지를 파싱한다.
from bs4 import BeautifulSoup as bs
from datetime import datetime

# 크롤링 후 결과를 데이터프레임 형태로 보기 위해 불러온다.
import pandas as pd
import time
from tqdm import tqdm

# 비동기적으로 콜러블을 실행하는 인터페이스를 제공한다.
import concurrent.futures

topic = 'finance' # technology
MAX_THREADS = 300


def scrape_info(url):
    re_titles = []
    re_contents = []
    re_dates = []

    # 크롤링 할 사이트
    try:
        res = requests.get(url[0], headers=headers)
        # print(res)
        res.raise_for_status()

        time.sleep(4)

        soup = bs(res.text, 'html.parser')
        news_list = soup.find_all('div', attrs={'class': 'column1 col col-10'})

        titles = news_list[0].select('.story-content > a > h3')
        contents = news_list[0].select('.story-content > p')
        dates = news_list[0].select('.article-time')

        for title, content, date in zip(titles, contents, dates):
            # print(title.text.strip())
            re_titles.append(title.text.strip())
            # print(content.text.strip())
            re_contents.append(content.text.strip())
            # print(date.text.strip())
            re_dates.append(date.text.strip())

        # print(len(re_titles), len(re_contents), len(re_dates))
        # for title, content, date in zip(re_titles, re_contents, re_dates):
        #     print(title, '\n', content, '\n', date, '\n')

    except:
        pass

    list_of_tuples = list(zip(re_titles, re_contents, re_dates))
    df = pd.DataFrame(list_of_tuples, columns=['title', 'content', 'date'])

    return df


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}

now = datetime.now()
today = now.strftime("%m_%d_%Y")
filename = "./" + "Reuters_News_URLs_" + topic + "_" + today + ".csv"
output_filename = "./" + "Reuters_News_" + topic + "_" + today + ".csv"

def get_stores(urls):

    threads = min(MAX_THREADS, len(urls))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for number, df in tqdm(zip(urls, executor.map(scrape_info, urls))):
            # print(output_filename)
            # print(number, df)
            df.to_csv(output_filename, index=False, mode='a', header=False, date_format='%Y%m%d', encoding='utf-8-sig')

            # (향후) 수집 정보를 보완한 후, 데이터베이스 테이블에 저장한다.
            # print(df)


if __name__ == '__main__':

    # 정보 가져오기
    t0 = time.time()

    # 파일 읽기
    df_URL = pd.read_csv(filename)
    urls = df_URL.values.tolist()

    get_stores(urls)
    t1 = time.time()
    print(f"{t1 - t0} seconds to get {len(urls)} stores.")

