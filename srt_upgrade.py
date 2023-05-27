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
import random

def web_wait(경로):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 경로)))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 경로)))
    except:
        print("에러")

def nextXpath(path):
    web_wait(path)
    return driver.find_element('xpath', path)

def checkTime(t):
    path = f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{t}]/td[4]/em'
    return driver.find_element('xpath', path)

def booking(t):
    path = f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{t}]/td[7]/a/span'
    return driver.find_element('xpath', path)

def nextLinkText(path):
    web_wait(path)
    return driver.find_element('link text', path)

print("SRT 예매 시도를 합니다.")
driver = webdriver.Chrome(executable_path="./chromedriver/chromedriver.exe")

# driver.maximize_window()  # 창 최대화
time.sleep(1)

## 열차표 예매 조건 설정
srt_id = get_secret("srt_id")
pw = get_secret("srt_pw")

# 도시 선택 옵션 번호
수서 = 'option[2]'
동탄 = 'option[3]'
천안아산 = 'option[5]'
오송 = 'option[6]'
익산 = 'option[15]'  
목포 = 'option[19]'
대전 = 'option[7]'
동대구 = 'option[10]'
신경주 = 'option[11]'
울산 = 'option[12]'
부산 = 'option[13]'

date = "29"
booking_time = "17:58"
출발역 = 익산 
도착역 = 수서

## SRT 홈피가서 로그인후 승차권 예매화면으로 이동
url = 'https://etk.srail.kr/main.do'
driver.get(url)
time.sleep(2)

# 팝업창 닫기
print("총 윈도우 개수 {0}".format(len(driver.window_handles)))
pop_up = len(driver.window_handles)

for i in range(pop_up - 1):
    print("{0}번째 팝업창 닫기".format(i + 1))
    
    driver.switch_to.window(
        driver.window_handles[1])  # 팝업창 선택후 닫기 (팝업창의 개수는 변경될 수 있음)
    time.sleep(0.5)
    driver.close()
    time.sleep(0.5)

driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화
nextXpath('//*[@id="wrap"]/div[3]/div[1]/div/a[2]').click()

# 로그인
print("로그인 시작")
nextXpath('//*[@id="srchDvNm01"]').send_keys(srt_id)
nextXpath(
    '/html/body/div[1]/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[1]/div[2]/input'
).send_keys(pw)
nextXpath(
    '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input'
).click()
print("로그인 종료후 팝업창 닫기")

print("총 윈도우 개수 {0}".format(len(driver.window_handles)))
pop_up2 = len(driver.window_handles)
for i in range(pop_up2 - 1):
    print("{0}번째 팝업창 닫기".format(i + 1))
    driver.switch_to.window(
        driver.window_handles[1])  # 팝업창 선택후 닫기 (팝업창의 개수는 변경될 수 있음)
    driver.close()

driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화

print("출발역과 도착역 선택")

출발지 = '//*[@id="dptRsStnCd"]/'+출발역
도착지 = '//*[@id="arvRsStnCd"]/'+도착역

nextXpath('//*[@id="dptRsStnCd"]').click()  #출발지 선택 버튼
nextXpath(출발지).click()  #출발지 선택

nextXpath('//*[@id="arvRsStnCd"]').click()  #도착지 선택 버튼
nextXpath(도착지).click()  #도착지 선택

print("달력 및 날짜 선택")
nextXpath(
    '//*[@id="search-form"]/fieldset/div[3]/div/input[2]').click()  #달력버튼 클릭
time.sleep(1)
driver.switch_to.frame('_LAYER_BODY_')  # Inner HTML Iframe 이동 (달력 창)
# time.sleep(1)
nextLinkText(date).click()
# time.sleep(2)

print("간편 조회버튼 클릭")
driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화

nextXpath(
    '//*[@id="search-form"]/fieldset/a').click()  # 간편조회하기 버튼
# time.sleep(3)

print("1페이지 서칭")
for i in range(1,100):
    try:
        print(checkTime(i).text)
        if checkTime(i).text == booking_time:
            for a in range(500):
                target1 = booking(i)
                if target1.text == "예약하기":
                    target1.click()
                    print("1순위 예약하였습니다. 시간 : {0}".format(datetime.datetime.now()))
                    Slack_Msg("1순위 예약에 성공하였습니다. 시간 : {0}".format(datetime.datetime.now()))
                    break
                else:
                    print(f"{a}번째 시도 - 매진 상태입니다. 시간 : {datetime.datetime.now()}")
                    # Slack_Msg("매진 상태입니다. 시간 : {0}".format(datetime.datetime.now()))
                    print("리프레쉬")
                    time.sleep(1)
                    driver.refresh()
                    print("=" * 20)
                    # random_interval = random.randint(1, 3)
                    # time.sleep(random_interval)
                    # print(f"반복 랜덤 인터벌 {random_interval}")
    except:
        pass
    
time.sleep(1)
print("2페이지 이동")
nextXpath('//*[@id="result-form"]/fieldset/div[8]/input').click()                 
time.sleep(3)

for i in range(1,100):
    try:
        
        print(checkTime(i).text)
        if checkTime(i).text == booking_time:
            for a in range(500):
                target1 = booking(i)
                print(target1.text)
                if target1.text == "예약하기":
                    target1.click()
                    print("1순위 예약하였습니다. 시간 : {0}".format(datetime.datetime.now()))
                    Slack_Msg("1순위 예약에 성공하였습니다. 시간 : {0}".format(datetime.datetime.now()))
                    break
                else:
                    print(f"{a}번째 시도 - 매진 상태입니다. 시간 : {datetime.datetime.now()}")
                    # Slack_Msg("매진 상태입니다. 시간 : {0}".format(datetime.datetime.now()))
                    print("리프레쉬")
                    time.sleep(1)
                    driver.refresh()
                    print("=" * 20)
                    # random_interval = random.randint(1, 3)
                    # time.sleep(random_interval)
                    # print(f"반복 랜덤 인터벌 {random_interval}")
    except:
        pass
              
print("전체 작업 종료")
