import pandas as pd
# requests는 작은 웹브라우저로 웹사이트 내용을 가져온다.
import requests
from datetime import datetime
from tqdm import trange

# BeautifulSoup 을 통해 읽어 온 웹페이지를 파싱한다.
from bs4 import BeautifulSoup as bs

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}
topic = 'finance' # technology
now = datetime.now()
today = now.strftime("%m_%d_%Y")
filename = "./" + "Reuters_News_URLs_" + topic + "_" + today + ".csv"


def make_url(pnums):
    global filename
    urls = []
    for pnum in trange(pnums):
        try:
            url = f'https://www.reuters.com/news/archive/{topic}news?view=page&page={pnum+1}&pageSize=10'
            urls.append(url)
        except:
            continue

    df = pd.DataFrame({'url': urls})
    df.to_csv(filename, index=False)


def get_url_status(pnum):
    url = f'https://www.reuters.com/news/archive/{topic}enews?view=page&page={pnum}&pageSize=10'

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()

        if res.status_code == 200:
            return True

        soup = bs(res.text, 'html.parser')
        error = soup.select_one('body > section > article > header > h2').text
        if error == "Server Encountered an Error":
            return False

    except Exception:
        pass

def last_pnum(pnums):
    left = 0
    right = pnums
    pnum = right
    for i in range(20):
        if get_url_status(pnum):
            left = pnum
            pnum = int((left + right) / 2)
        else:
            right = pnum
            pnum = int((left + pnum) / 2)
    return pnum


pnums = 100000
if __name__ == '__main__':
    pnums = last_pnum(pnums)
    print(pnums)
    make_url(pnums)

