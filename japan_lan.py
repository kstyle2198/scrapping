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
# from secret import *

## 오늘 날짜로부터 과거 5일치 일본어 회화를 슬랙으로 보내주기

today = datetime.datetime.today().date()
기준일 = datetime.date(2021, 10, 3)
gap = today - 기준일
today_num = 3254 + gap.days * 2
Slack_Msg("==================")
Slack_Msg("==================")
Slack_Msg("==================")

for i in range(1):

    time.sleep(1)
    today_num -= i * 2
    url = 'https://audioclip.naver.com/channels/164/clips/{0}'.format(
        str(today_num))
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

print("전체 작업 종료")