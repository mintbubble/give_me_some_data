import requests
import json
import pandas

url = 'https://www.sberbank.ru/common/img/uploaded/redirected/s_m_business/franchises/main/data/data.json'

headers = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'accept': 'application/json, text/plain, */*',
    'referrer': 'https://www.sberbank.ru/ru/s_m_business/franchises',
    'referrerPolicy': 'strict-origin-when-cross-origin',
}

test = requests.get(url, headers=headers)
result = json.loads(test.text)
all_franchises = result['app']['filter']['items']

for i in all_franchises:
    name = i['link'].split('/')[-1].strip()
    try:
        test1 = requests.get(
            f'https://www.sberbank.ru/common/img/uploaded/redirected/s_m_business/franchises/detail/{name}/data/data.json',
            headers=headers)
        i['requirements_list'] = json.loads(test1.text)['app']['requirements']['list']
        i['requirements_points'] = json.loads(test1.text)['app']['requirements']['points']
    except Exception as e:
        print(name, e)

res = pandas.DataFrame.from_dict(all_franchises)
res.to_excel('sberbank_all_franchises.xlsx')

print('\nDONE')