import time, random
import CrawlingHandler as CH

def createFile(fname):
    fp = open(fname+".json", 'w', encoding='utf-8')
    fp.write("[\n")
    return fp

def writeFile(fp, newData, flag=1):
    if flag == 1:
        print("Start summary File Write")
    else:
        print("Start non summary File Write")
    fp.write("    {\n")
    fp.write('        "title": ' + '"' + newData.getTitle() + '",\n')
    fp.write('        "category": ' + '"' + newData.getCategory() + '",\n')
    fp.write('        "url": ' + '"' + newData.getUrl() + '",\n')
    fp.write('        "summary": ' + '"' + newData.getSummary() + '",\n')
    fp.write('        "contents": ' + '"' + newData.getContents() + '",\n')
    fp.write("    },\n")

def closeFile(fp):
    fp.seek(fp.tell() - 3)
    fp.write("\n")
    fp.write("]")
    fp.close()

base_url = "https://www.hankyung.com/all-news?page="

for i in range(1, 150000):
    if i%10000 == 1:
        fp_summary = createFile('summary'+str(i))
        fp_non_summary = createFile('non_summary'+str(i))
    url = base_url+str(i)
    print(url)
    extracted_url = CH.extract_link(url)
    for ref in extracted_url:
        print('page: '+str(i), ref)
        newData = CH.CrawledDataHandler(ref)
        time.sleep(random.uniform(i%4, i%4+2))
        try:
            newData.crawling()
            if CH.checkValue(newData) is False:
                continue
        except:
            continue

        if newData.getSummary() != "None":
            writeFile(fp_summary, newData)
        else:
            writeFile(fp_non_summary, newData, 0)
    if i%10000 == 0:
        closeFile(fp_summary)
        closeFile(fp_non_summary)

print("Processing complete\n")

