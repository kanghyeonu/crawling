import time, random
import CrawlingHandler as CH

def createFile(fname):
    fp = open(fname+".json", 'w', encoding='utf-8')
    fp.write("[\n")
    return fp

def writeFile(fp, newData):

    print("File Write")

    fp.write("    {\n")
    fp.write('        "title": ' + '"' + newData.getTitle() + '",\n')
    fp.write('        "category": ' + '"' + newData.getCategory() + '",\n')
    fp.write('        "url": ' + '"' + newData.getUrl() + '",\n')
    fp.write('        "summary": ' + '"' + newData.getSummary() + '",\n')
    fp.write('        "contents": ' + '"' + newData.getContents() + '"\n')
    fp.write("    },\n")

def closeFile(fp):
    fp.seek(fp.tell() - 3)
    fp.write("\n")
    fp.write("]")
    fp.close()

base_url = "https://www.sedaily.com/NewsList/GD01/New/"

for i in range(1, 701):
    if i == 1:
        fp = createFile('seoulkyungje_industry'+str(i))

    url = base_url+str(i)
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
            print("except")
            continue

        writeFile(fp, newData)

closeFile(fp)

print("Processing complete\n")

