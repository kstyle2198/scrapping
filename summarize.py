## gensim을 활용해 네이버 뉴스를 요약

from bs4 import BeautifulSoup
import requests
# pip3 install gensim==3.6.0
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
}


def get_only_text(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status
    soup = BeautifulSoup(res.text, "lxml")
    title = soup.title.get_text()
    content = soup.find("div", {
        "id": "articleBodyContents"
    }).get_text().strip()
    return title, content


## navar 뉴스 링크
# url = "https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=101&oid=014&aid=0004712835"
url = "https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=104&oid=028&aid=0002561228"
target = get_only_text(url)
print(len(target[1]))
print(target[1])
print("=" * 20)
print("title : " + target[0])
print("Summary : ")
summary = summarize(repr(target[1]), word_count=90)
print(summary)
print(len(summary))
