import requests
import json
from bs4 import BeautifulSoup
import re
import pandas

###
url = 'http://sro.gosnadzor.ru/?arrFilter_ff%5BNAME%5D=&arrFilter_pf%5BREGISTR_NUMBER%5D=&arrFilter_pf%5BINN%5D=&arrFilter_pf%5BSTATUS_SRO%5D=10&arrFilter_pf%5BTYPE_SRO%5D%5B%5D=321&arrFilter_pf%5BTYPE_SRO%5D%5B%5D=199&arrFilter_pf%5BTYPE_SRO%5D%5B%5D=322&set_filter=&set_filter=Y'
test = requests.get(url)
res = [i for i in test.text.split('\n') if 'gridData' in i]
text0 = res[0].replace('\t', '').replace('gridData: ', '')[:-1]
orgs = json.loads(text0.replace('\'', '\"'))

###
for i in orgs:
    try:
        kid = requests.get('http://sro.gosnadzor.ru' + i['FULL_NAME'].split('\"')[1])
        soup = BeautifulSoup(kid.text)
        mydivs = soup.findAll("div", {"id": "sro-main-info"})
        ll = re.findall('ИНН:.+ОГРН', mydivs[0].text.replace('\n', '').replace('\t', ''))
        i['INN'] = int(ll[0].replace('ИНН:', '').replace('ОГРН', ''))
        print()
    except Exception as e:
        print(i, e)
        continue

result = pandas.DataFrame.from_dict(orgs)
result.to_excel('gosnadzor_orgs.xlsx')
print('\nDONE')
