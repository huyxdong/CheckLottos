import logging
import json
import argparse
import sys
import requests
import psycopg2

from datetime import datetime as dt
from datetime import timedelta, date
from config import config
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.WARNING)


def crawl(url):
    r = requests.get(url)
    if r.status_code != 200:
        sys.exit()
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        table = soup.find(id="result_tab_mb").tbody.find_all("tr")
    except AttributeError:
        return logging.error(f"Ngày hôm nay {url[-10:]} không có kết quả xổ số")
    for index, ele in enumerate(table):
        logging.debug(ele)
        # Reward name: "Đặc biệt", "Giải nhất"...
        reward = ele.find_all("td")[0].string

        if len(results) == 8:
            break
        if reward:
            results[reward] = list()

        for i in ele.find_all("td")[1:]:
            logging.debug(i.string)
            if reward:
                results[reward].append(i.string)
            else:
                results[table[index - 1]
                        .find_all("td")[0].string].append(i.string)

    return results


def insert_lotto_result(results, date, thongke=False):
    if not thongke:
        sql = '''INSERT INTO lottos.ketqua (results, date) VALUES (%s, %s)'''
    else:
        sql = '''INSERT INTO lottos.thongke (results, date) VALUES (%s, %s)'''
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (results, date))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def fetch_lottos_result(date):
    """Check if result of day does exist"""
    pass


def crawl_list_of_date(*args, **kwargs):

    def daterange(date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + timedelta(n)

    start_dt = args[0]
    end_dt = args[1]
    for dt in daterange(start_dt, end_dt):
        date = dt.strftime("%d-%m-%Y")
        url = f"https://ketqua.net/xo-so-truyen-thong.php?ngay={date}"
        results = crawl(url)
        insert_lotto_result(json.dumps(results, ensure_ascii=False), dt, True)


if __name__ == "__main__":
    # today = dt.today().date()  # datetime.date(2019, 7, 19)
    results = dict()
    url = "https://ketqua.net"
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-d", "--date", type=str,
    #                     help="choose a specific date for displaying lotto results",)
    # args = parser.parse_args()
    # date = args.date  # 27-06-2019
    # if date:
    #     url = f"https://ketqua.net/xo-so-truyen-thong.php?ngay={date}"
    # results = crawl(url)
    # insert_lotto_result(json.dumps(results, ensure_ascii=False), today)
    start_dt = date(2019, 2, 4)
    end_dt = date(2019, 7, 1)
    crawl_list_of_date(start_dt, end_dt)
