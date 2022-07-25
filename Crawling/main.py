import time, random
import CrawlingHandler as CH

def createFile(fname):
    fp = open(fname+".json", 'w', encoding='utf-8')
    fp.write("[\n")
    return fp

def writeFile(fp, newData):

    print("File Write")

    fp.write("\t{\n")
    fp.write('\t\t"title": ' + '"' + newData.getTitle() + '",\n')
    fp.write('\t\t"category": ' + '"' + newData.getCategory() + '",\n')
    fp.write('\t\t"url": ' + '"' + newData.getUrl() + '",\n')
    fp.write('\t\t"summary": ' + '"' + newData.getSummary() + '",\n')
    fp.write('\t\t"contents": ' + '"' + newData.getContents() + '"\n')
    fp.write("\t},\n")

def closeFile(fp):
    fp.seek(fp.tell() - 3)
    fp.write("\n")
    fp.write("]")
    fp.close()

base_url = "https://www.sedaily.com/NewsList/GC01/New/"
for i in range(1, 301):
    if i == 1:
        fp = createFile('seoulkyungje_society'+str(i))

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

