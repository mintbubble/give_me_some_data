import requests
import xml.dom.minidom as xdm
from datetime import datetime

headers = {'Host': 'cargo-report.info',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'Accept': 'text/plain, */*; q=0.01',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest',
           'Content-Length': '6',
           'Origin': 'https://cargo-report.info',
           'Connection': 'keep-alive',
           'Referer': 'https://cargo-report.info/info/wagon-owner/',
           'Cookie': 'PHPSESSID=el0eocd6gdhie5rh8u1vi2um7c; _ga=GA1.2.90585942.1575837864; _gid=GA1.2.1767646151.1575837864'
           }
data_result = []
r = xdm.parse('vagons.xml')
node_list = r.getElementsByTagName('option')
vagons_type_name = [i._get_firstChild().data for i in node_list]
vagon_types = list(map(int, [i._attrs['value']._value for i in node_list]))
print()
for i, val in dict(zip(vagon_types, vagons_type_name)).items():
    res = requests.post('https://cargo-report.info/includes/ajax_search_wagon_owner.php', data={'type': i},
                        headers=headers)
    f = True
    text = res.text
    while f:
        x = text.find('<td>')
        if x < 0:
            f = False
        else:
            y = text.find('</td>')
            n = text[y + 1:].find('<td>')
            m = text[y + 1:].find('</td>')
            data_result.append(f'{val};{text[x + 4:y]};{text[y + 1:][n + 4:m]}\n')
            text = text[y + 1:][m + 1:]

with open(f'cargo_report_wagon_owners_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.txt', 'a', encoding='utf-8') as f:
    for line in data_result:
        f.write(line)
print('done')
