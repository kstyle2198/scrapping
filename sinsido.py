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
from config import get_secret

def nextXpath(path):
    return driver.find_element('xpath', path)

print("신시도 예매 시도를 합니다.")
driver = webdriver.Chrome(executable_path="./chromedriver/chromedriver.exe")

# driver.maximize_window()  # 창 최대화
time.sleep(1)

## 열차표 예매 조건 설정
id = get_secret("sinsido_id")
pw = get_secret("sinsido_pw")

## 홈피가서 로그인
url = 'https://www.foresttrip.go.kr/indvz/main.do?hmpgId=0301'
driver.get(url)
time.sleep(3)
nextXpath('//*[@id="header"]/div[1]/form/div[2]/a[1]').click()

time.sleep(3)
nextXpath('//*[@id="mmberId"]').send_keys(id)
nextXpath('//*[@id="gnrlMmberPssrd"]').send_keys(pw)
nextXpath('//*[@id="infoWrap"]/fieldset/div/div[1]/input[3]').click()
time.sleep(3)

nextXpath('//*[@id="GNB001"]/a').click()
nextXpath('//*[@id="GNB001003001"]/a').click()
time.sleep(3)

print("작업종료")