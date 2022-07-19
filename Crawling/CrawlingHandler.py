import requests, re
from bs4 import BeautifulSoup

all_char = re.compile('[^가-힣a-zA-b0-9\(\)\[\]\{\}\<\>△=;&┤│┼├|\~\-\+:\.@ !"\'?/#$%^&\*_\-]')

qm = re.compile('"+')
only_eng = re.compile('[A-Za-z]{46,}]')

constraint0 = re.compile('\{.*?\}|\[.*?\]')
constraint1 = re.compile('<.*=.*?>|<.*뉴스.*?>')
constraint2 = re.compile('&.*?;')
constraint3 = re.compile('\(:.*?:\)|\(.*?\)')
constraint4 = re.compile('사진=.*? ')
constraint5 = re.compile('[가-힣 /]{3,8} 기자')
constraint6 = re.compile('속보=')
constraint7 = re.compile('([0-9]{3})?-[0-9]{3,4}-[0-9]{4}')

constraints = [constraint0, constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, constraint7]
constraints2 = ['|', '-', '+', ':', '~']

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
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
        response = requests.get(self.url, headers=headers)  # url 정보를 가져옴

        if response.status_code == 200:  # url 정보를 받는 데 성공한 경우
            pass
        else:
            print(response.status_code)  # url 이 없을 경우 상태 코드 출력
            return
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')  # html 문서로 파싱

        # 한국 경제
        figures = soup.find_all('figure')
        for figure in figures:
            soup.figure.extract()
        title = soup.select_one('#container > div > div > article > h1').get_text()
        category = soup.select_one('#wrap > header > div > div.header-section-cont > div.section-gnb-wrap > h1 > a.section-title').get_text()
        summary = soup.select_one('#container > div > div > article > div > div > div.article-body-wrap > div.summary')
        contents = soup.select_one("#articletxt").get_text()

        if summary is None:
            summary = "None"

        self.summary = self.preprocessing(summary.get_text())
        self.title = self.preprocessing(title)
        self.category = self.preprocessing(category)
        self.contents = self.preprocessing(contents)

        self.displayData()

    def displayData(self):
        print(self.title)
        print(self.category)
        print(self.summary)
        print(self.contents)

    def preprocessing(self, string):
        #기본적인 1차 전처리
        fixed_str = all_char.sub(' ', string)  # 특수문자 제거
        fixed_str = " ".join(fixed_str.split()) #다수 공백 및 문자열 양끝 공백제거

        #조건이 요구하는 필수 사항들 삭제
        for i in constraints:
            fixed_str = i.sub('', fixed_str)
        fixed_str = qm.sub('"', fixed_str)

        #문장 단위별로 요구 사항 삭제
        fixed_list = list(fixed_str.split(' '))
        for i in range(len(fixed_list)):
            fixed_list[i] = fixed_list[i].lstrip('.')
            fixed_list[i] = fixed_list[i].lstrip('—')
            fixed_list[i] = fixed_list[i].lstrip('A.')
            if fixed_list[i].count('학교') > 8 or fixed_list[i].count('△') > 10 or '@' in fixed_list[i]:
                fixed_list[i] = ' '
                continue
            for j in constraints2:
                if fixed_list[i].count(j) > 5:
                    fixed_list[i] = ' '
                    break

        fixed_str = " ".join(fixed_list)
        fixed_str = " ".join(fixed_str.split())

        return fixed_str

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
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    div_list = soup.find_all("h3", class_ = "tit")
    for div in div_list:
        list_href.append(div.find("a")["href"])

    return list_href

# 새로운 객체가 정보를 제대로 가지고 있는 지 확인
def checkValue(newValue: CrawledDataHandler) -> bool:
    if newValue.getTitle() is None:
        print('Title is empty')
        return False
    if newValue.getCategory() is None:
        print('Category is empty')
        return False
    if newValue.getContents() is None:
        print('Contents is empty')
        return False
    if newValue.getSummary() is None:
        newValue.summary = "None"
    return True