import CrawlingHandler as CH

#결과가 출력될 파일
f = open('result.json', 'w')
f.write("[\n")

base_url = "https://www.hankyung.com/all-news?page="

for i in range(1, 150000):
    url = base_url+str(i)

    extracted_url = CH.extract_link(url)
    for ref in extracted_url:
        print(i, ref)
        newData = CH.CrawledDataHandler(ref)
        try:
            newData.crawling()
            if CH.checkValue(newData) is False:
                continue
        except:
            continue

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

