from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import datetime
from slack import *

## 오늘 날짜로부터 과거 00일치 일본어 회화를 슬랙으로 보내주기

today = datetime.datetime.today().date()
기준일 = datetime.date(2021, 10, 3)
gap = today - 기준일
today_num = 3254 + gap.days * 2
Slack_Msg("==================")
Slack_Msg("==================")
Slack_Msg("==================")

jp_url = 'https://audioclip.naver.com/channels/164/clips/'
cn_url = 'https://audioclip.naver.com/channels/165/clips/'

lan_lst = [jp_url]   #, cn_url
cn_add = 0

for lan in lan_lst:
    i = 0  # 최신 클립만 조회

    time.sleep(1)
    today_num -= i * 2
    url = lan + '{0}'.format(str(today_num + cn_add))
    driver = webdriver.Chrome(
        executable_path="./chromedriver/chromedriver.exe")
    time.sleep(1)
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_xpath(
        '//*[@id="content"]/div/section/div[2]/div[1]/button[2]/span').click()
    time.sleep(1)

    title = driver.find_element_by_xpath(
        '//*[@id="content"]/div/section/div[1]/div[2]/h3').text
    print(title)
    Slack_Msg(title)
    print("=" * 30)
    text = driver.find_element_by_xpath(
        '//*[@id="chapter"]/div/ul/li[1]/p').text
    print(text)
    Slack_Msg(text)
    Slack_Msg("==================")

    driver.close()

    cn_add += 5  # 오늘자 중국어 회화 찾기 위한 날짜 조정 변수

print("전체 작업 종료")