import json
import pandas
import requests
from datetime import datetime

test_r = requests.get(
    'http://map.patriarchia.ru/api/index.php?token=c2cbe8cd873f8e4751a7f7bb5292e68a&country=ru&church=&ctype=0&t=0&s=&params=[]&_=1597398154200')
rez = json.loads(test_r.text)
# coord_id = {i['id']: i['geometry']['coordinates'] for i in rez['features']}
# name_id = {i['id']: i['properties']['hintContent'] for i in rez['features']}

orgs_id = {i['id']: {'Name': i['properties']['hintContent'],
                     'coordinates': i['geometry']['coordinates'],
                     'lat': i['geometry']['coordinates'][0],
                     'long': i['geometry']['coordinates'][1]} for i in
           rez['features']}
df = pandas.read_json(json.dumps(orgs_id))
df.T.to_excel(f'patriarchia_coordinates_{datetime.now().strftime("%d.%m.%Y_%H.%M.%S")}.xlsx')
# test_text = requests.get('http://map.patriarchia.ru/api/index.php?token=c2cbe8cd873f8e4751a7f7bb5292e68a&m=info&msg=1&id=28169&urlmode=1&lang=ru&_=1597332819417')

print('DONE\n\n\n')
