import pandas as pd
import pymongo
import time

from datetime import datetime


topic = 'finance' # technology
now = datetime.now()
today = now.strftime("%m_%d_%Y")
filename = "./" + "Reuters_News_" + topic + "_" + today + ".csv"

if __name__ == '__main__':
    # 정보 가져오기
    t0 = time.time()

    # 파일 읽기
    df_news = pd.read_csv(filename)
    news = df_news.values.tolist()

    client = pymongo.MongoClient('mongodb+srv://root:4team123!@192.168.54.254/test?retryWrites=true&w=majority')
    db = client.db.news
    try:
        db.insert_many(news)
        print(f'inserted {len(news)} articles')
    except:
        print('an error occurred news were not stored to db')

    t1 = time.time()
    print(f"{t1 - t0} seconds to store {len(news)} stores.")