import requests
import re
from bs4 import BeautifulSoup
import json
import pandas
from datetime import datetime

u = r'http://www.patriarchia.ru/db/organizations/'

test = requests.get(u)
soup = BeautifulSoup(test.text, 'lxml')
rez_all = soup.findAll("div", {"class": "main"})

rez = re.findall('<h4 class="title" style="margin-bottom:0px;">.*</a></h4>', str(rez_all[0]))

names = [i.split('html">')[1].replace('</a></h4>', '') for i in rez]
urls = ['http://www.patriarchia.ru' + i.split('html">')[0].replace(
    '<h4 class="title" style="margin-bottom:0px;"><a href="', '') + 'html' for i in rez]
obj = dict(zip(names, urls))
obj_text = {}
error_list = {}

for k, value in obj.items():
    test1 = requests.get(value)
    tsoup = BeautifulSoup(test1.text, 'lxml')
    try:
        obj_text[k] = {'url': value,
                       'text': re.findall('<meta content=.*name="description"/>', str(tsoup.head))[0] \
                           .replace('<meta content=', '') \
                           .replace('name="description"/', '')
                       }
    except IndexError:
        error_list[k] = value
df = pandas.read_json(json.dumps(obj_text))
df.T.to_excel(f'patriarchia_organizations_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.xlsx')
print('DONE\n\n\n')
print(error_list)
