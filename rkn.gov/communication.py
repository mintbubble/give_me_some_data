import requests
import re
import pandas
import datetime

superresult = []
for k in range(0, 4981, 20):
    print(k)
    test = requests.get(f'https://rkn.gov.ru/communication/register/radio/radio/p{k}/?order=&year=#formtabs-2',
                        headers={
                            'Host': 'rkn.gov.ru',
                            'Connection': 'keep-alive',
                            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                            'sec-ch-ua-mobile': '?0',
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                            'Sec-Fetch-Site': 'same-origin',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-User': '?1',
                            'Sec-Fetch-Dest': 'document',
                            # 'Referer': ' https://rkn.gov.ru/communication/register/radio/radio/p1/?order=&year=',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Cookie': 'sp_test=1; csrf-token-name=csrftoken; PHPSESSID=8redca1ldj45cq2tv09fsu6bf2; _ym_uid=162997280082319804; _ym_d=1629972800; _ym_isad=2; sputnik_session=1629972409452|19; csrf-token-value=169ed4ba9c1612986f383711969345a2e3a97953595d21be14e14611195da5e71535d0d710445f31'
                        })

    text_ = re.sub('[\r\n|\n|\r]', '', test.text)
    res = re.findall("<tr class='clmn1' >.*</tr>", text_.replace('  ', ''))[0]
    res = res[:res.find('</table>')]
    res1 = [i[5:] for i in res.split("<tr class='clmn") if i != '']
    for i in res1:
        superresult.append(
            [j.replace('</td>', '').replace('class="t1"', '').replace('align="right"', '').replace('<nobr>',
                                                                                                   '').replace(
                '</nobr>', '').replace('>', '').strip() for j in i.split('<td')])
        # re.sub("""['</td>'|'class="t1"'|'align="right"'|'<nobr>'|'</nobr>']""",'',j)

df = pandas.DataFrame(superresult)
df.to_excel(f'rkn_gov_{datetime.datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.xlsx')

print('\n\n\nDONE')
