import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
           'Sec-Fetch-User': '?1',
           'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'Sec-Fetch-Site': 'same-origin',
           'Sec-Fetch-Mode': 'navigate',
           'Referer': 'https://www.logistics1520.com/owners-wagons-group/1/4',
           'Cookie': 'mobuser2017=yes; PHPSESSID=0k22iubcu1tmfqnlvi1r7dcrs2; _ym_uid=1574774903271382424; _ym_d=1574774903; _ym_visorc_54102274=w; _ym_isad=1; _ga=GA1.2.2080635541.1574774904; _gid=GA1.2.1614511813.1574774904; _gat_gtag_UA_142325730_1=1',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
           }


def link(line):
    v = {}
    l = line.split('"')
    v[l[5].split('&')[0]] = l[1]
    return v


def get_vagon(rezult):
    vagon = []
    for line in rezult:
        if 'owner-wagons-detail' in line or 'owners-wagons-detail' in line:
            vagon.append(link(line))
    return vagon


groups = dict(zip([1, 2, 3, 4, 5, 6, 8], [4, 14, 9, 16, 24, 2, 18]))
vagon_type = ['', 'Зерновозы', 'Крытые', 'Платформы', 'Полувагоны', 'Прочие', 'Рефрижераторы', '', 'Цистерны']
rezult = {}
for g, i in {8: 18}.items():  # groups.items():
    rez = []
    for ii in range(1, i + 1):
        url = f'https://www.logistics1520.com/owners-wagons-group/{g}/{ii}'
        res = requests.get(url,
                           # headers=headers,
                           verify=False)
        rez.extend(get_vagon([i for i in res.text.split('\n')]))
    rezult[vagon_type[g]] = rez


def get_all_vagons(test):
    soup = BeautifulSoup(test, 'lxml')
    lt = [line.replace('\t', '').strip() for line in soup.text.split('\n') if line != '']
    n = lt.index('Типы вагонов')
    mm = []
    for line in lt[n + 1:]:
        if 'Торговая площадка' not in line and line != '':
            mm.append(line)
        else:
            break
    return mm


to_write = {}
x = 0
for gr, orgs in rezult.items():
    for org in orgs:
        for name, lnk in org.items():
            test = requests.get(f'https://www.logistics1520.com{lnk}', verify=False).text
            vagons_list = get_all_vagons(test)
            to_write[x] = {'name': name, 'link': lnk, 'group': gr, 'vagons_list': vagons_list}
            x += 1

with open(f'logistics1520_cistern_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.txt', 'a') as f:
    for index, org in to_write.items():
        for item in org['vagons_list']:
            f.write(f'{org["name"]};{org["link"]};{org["group"]};{item}\n')
print('done')
