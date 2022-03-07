import requests
import json
from bs4 import BeautifulSoup
import pandas

url = 'http://sro.gosnadzor.ru/'
test = requests.get(url)
res = [i for i in test.text.split('\n') if 'gridData' in i]
text0 = res[0].replace('\t', '').replace('gridData: ', '')[:-1]
orgs = json.loads(text0.replace('\'', '\"'))

for i in orgs:
    try:
        kid = requests.get('http://sro.gosnadzor.ru/sro_detail.php?ID=' + str(i['ID']))
        soup = BeautifulSoup(kid.text)
        mydivs = soup.findAll("div", {"id": "tab_3"})
        tt = mydivs[0].text.replace('\t', '').split('\n\n')
        res__ = dict(zip([f'col_{i}' for i in range(1, len(tt) + 1)], tt))
        i.update(res__)
        mydivs1 = soup.findAll("div", {"id": "tab_1"})
        tt1 = mydivs1[0].text.replace('\t', '').split('\n\n')
        res1__ = dict(zip([f'col_{i}' for i in range(100, 100 + len(tt) + 1)], tt1))
        i.update(res1__)
    except Exception as e:
        print(i['ID'], e)
        continue

result_ = pandas.DataFrame.from_dict(orgs)
result_.to_excel('gosnadzor_orgs_detail.xlsx')
print('\nDONE')
