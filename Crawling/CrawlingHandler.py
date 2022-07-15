import requests
from bs4 import BeautifulSoup

#한국 경제 전용
class CrawledDataHandler:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.category = None
        self.summary = None
        self.contents = None

    def crawling(self):
        # Crawling 하고 싶은 사이트에게 유저 정보를 넘겨 접근 거부를 방지
        # http://www.useragentstring.com/ 사이트 내에 있는 Mozilla ~~ 부분
        headers = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

        response = requests.get(self.url, headers=headers)  # url 정보를 가져옴

        if response.status_code == 200:  # url 정보를 받는 데 성공한 경우
            pass
        else:
            print(response.status_code)  # url 이 없을 경우 상태 코드 출력
            return
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')  # html 문서로 파싱

        # 한국 경제
        title = soup.select_one('#container > div > div > article > h1').get_text()
        category = soup.select_one('#wrap > header > div > div.header-section-cont > div.section-gnb-wrap > h1 > a.section-title').get_text()
        summary = soup.select_one('#container > div > div > article > div > div > div.article-body-wrap > div.summary').get_text()

        string = ""
        div_list = soup.find_all("div", class_="article-body")
        print(*div_list)
        for div in div_list:
            string += div
        #contents = soup.select_one("#articletxt").get_text().strip()

        # title = self.preprocessing(title)
        # category = self.preprocessing(category)
        # summary = self.preprocessing(summary)
        # contents = self.preprocessing(contents)

        # 데이터 확인
        print(title)
        print(category)
        print(summary)
        print(string)

        # 객체에 데이터 저장
        self.title = title
        self.category = category
        self.summary = summary
        self.contents = string



    def preprocessing(self, string):
        temp = ""
        return temp

    # 클래스 기본 함수
    def getTitle(self):
        return self.title

    def getCategory(self):
        return self.category

    def getSummary(self):
        return self.summary

    def getContents(self):
        return self.contents

def extract_link(url):
    list_href = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    div_list = soup.find_all("h3", class_ = "tit")
    for div in div_list:
        list_href.append(div.find("a")["href"])

    return list_href

# 새로운 객체가 정보를 제대로 가지고 있는 지 확인
def checkValue(newValue: CrawledDataHandler) -> bool:
    if newValue.getTitle() is None:
        return False
    if newValue.getCategory() is None:
        return False
    if newValue.getSummary() is None:
        return False
    if newValue.getContents() is None:
        return False
    return True