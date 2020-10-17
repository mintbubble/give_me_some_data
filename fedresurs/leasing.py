import requests
import pandas
import json
from datetime import datetime

test = requests.get(
    'https://fedresurs.ru/backend/encumbrances?startIndex=0&pageSize=9758&additionalSearchFnp=true&searchString=%D0%BB%D0%B8%D0%B7%D0%B8%D0%BD%D0%B3',
    params={
        'group': 'Leasing',
        'publishDateStart': '2019-08-01',
        'publishDateEnd': '2019-09-01'
    },
    headers={
        'authority': 'fedresurs.ru',
        'pragma': 'no-cache',
        'cache-control': 'no-cach',
        'accept': 'application/json, text/plain, */*',
        'dnt': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://fedresurs.ru/search/encumbrances?searchString=%25D0%25BB%25D0%25B8%25D0%25B7%25D0%25B8%25D0%25BD%25D0%25B3&group=Leasing&publishPeriod=%257B%2522beginJsDate%2522%253A%25222019-08-01T00%253A00%253A00.000Z%2522%252C%2522endJsDate%2522%253A%25222019-09-01T00%253A00%253A00.000Z%2522%257D&attempt=3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'fedresurscookie=ecfc54e16552deb94a8e93f5b9b56c60; _ym_uid=1573421014808015745; _ym_d=1573421014; _ym_visorc_44970568=w; _ym_isad=1'
    }
)

data = json.loads(test.text)['pageData']
df = pandas.read_json(json.dumps(data))
df.to_excel(f'fedresurs_leasing_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.xlsx')
