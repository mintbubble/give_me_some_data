import requests
import json
import pandas

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json;charset=UTF-8",
    "sessionid": "b4b5adc0-8a02-11e5-fd30-3aa488f7bee7",
    "x-kl-ajax-request": "Ajax_Request"}

tasks = []
for i in range(1, 233):
    ss1 = "{\"subjectId\":\"2\",\"levelIds\":[],\"themeIds\":[],\"typeIds\":[],\"id\":\"\",\"favorites\":0,\"answerStatus\":0,\"themeSectionIds\":[],\"published\":0,\"extId\":\"\",\"fipiCode\":\"\",\"docId\":\"\",\"isAdmin\":false,\"loadDates\":[],\"isPublished\":false,\"pageSize\":5,\"pageNumber\":\"%i\"}" % i
    test = requests.post('http://os.fipi.ru/api/tasks',
                         headers=headers,
                         data=ss1)
    tasks.extend(json.loads(test.text)['tasks'])

res = pandas.read_json(json.dumps(tasks))
res.to_csv('os_fipi_tasks.csv')
print('DONE')
