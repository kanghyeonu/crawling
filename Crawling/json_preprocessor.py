import json
import CrawlingHandler as CH


f = open('seoulkyungje_economy1.json', encoding='utf-8')
data = json.load(f)
for i in data:
    print(i['title'])
    print(i['category'])
    print(i['url'])
    print(i['contents'])
    print()



f.close()
