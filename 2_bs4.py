import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
# print(soup.title)
# print(soup.title.get_text())

rank1 = soup.find("li", attrs={'class':'rank01'})
print(rank1.get_text().strip()[0:-1])
# rank2 = rank1.next_sibling.next_sibling
# print(rank2.get_text())
# print(rank1.find_next_siblings("li"))

# cartoons = soup.find_all("a", attrs={'class':'title'})
# lists= []
# for cartoon in cartoons:
#     title = cartoon.get_text()
#     link = "https://comic.naver.com"+cartoon['href']
#     print(title, link)
    # lists.append(cartoon.get_text())

# print(len(lists))

###
# dust = soup.find("div", attrs = {"class" : "kkk", "id": "gdf"}, text = ["단어1", "단어2"])

