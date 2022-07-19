import time, random
import CrawlingHandler as CH

#결과가 출력될 파일
f = open('result.json', 'w', encoding="utf-8")
f.write("[\n")

base_url = "https://www.hankyung.com/all-news?page="

for i in range(1, 150000):
    url = base_url+str(i)
    print(url)
    extracted_url = CH.extract_link(url)
    for ref in extracted_url:
        print('page: '+str(i), ref)
        newData = CH.CrawledDataHandler(ref)
        #time.sleep(random.uniform(i%4, i%4+2))
        try:
            newData.crawling()
            if CH.checkValue(newData) is False:
                print('empty')
                continue
        except:
            continue

        print("Start File Write")
        f.write("    {\n")
        f.write('        "title": ' + '"' + newData.getTitle() + '",\n')
        f.write('        "category": ' + '"' + newData.getCategory() + '",\n')
        f.write('        "url": ' + '"' + ref + '",\n')
        f.write('        "summary": ' + '"' + newData.getSummary() + '",\n')
        f.write('        "contents": ' + '"' + newData.getContents() + '",\n')
        f.write("    },\n")

f.seek(f.tell()-3)
f.write("\n")
f.write("]")
f.close()

print("Processing complete\n")

