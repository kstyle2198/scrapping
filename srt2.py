from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
import time
import datetime
from slack import *
from config import get_secret
import random
from selenium.webdriver.support.select import Select


### 변수정리 #####
srt_id = get_secret("srt_id")
pw = get_secret("srt_pw")

# 도시 선택 옵션 번호
수서 = 'option[2]'
동탄 = 'option[3]'
천안아산 = 'option[32]'
오송 = 'option[23]'
익산 = 'option[25]'  
목포 = 'option[15]'
대전 = 'option[12]'
동대구 = 'option[13]'
신경주 = 'option[20]'
울산통도사 = 'option[24]'
부산 = 'option[17]'

date = "20240303"
booking_time = "17:59"
출발역 = 익산
도착역 = 수서

출발지 = '//*[@id="dptRsStnCd"]/'+출발역
도착지 = '//*[@id="arvRsStnCd"]/'+도착역

### 함수정리 #####

def web_wait(경로):
    global driver
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 경로)))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 경로)))
    except:
        print("에러")

def nextXpath(path):
    global driver
    web_wait(path)
    return driver.find_element('xpath', path)

def checkTime(t):
    global driver
    path = f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{t}]/td[4]/em'
    return driver.find_element('xpath', path)

def booking(t):
    global driver
    path = f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{t}]/td[7]/a/span'
    return driver.find_element('xpath', path)

def nextLinkText(path):
    global driver
    web_wait(path)
    return driver.find_element('link text', path)

def 팝업창닫고기본창활성화():
    global driver
    pop_up = len(driver.window_handles)
    print("총 윈도우 개수 {0}".format(pop_up))

    for i in range(pop_up - 1):
        print("{0}번째 팝업창 닫기".format(i + 1))
        driver.switch_to.window(driver.window_handles[1])  # 팝업창 선택후 닫기 (팝업창의 개수는 변경될 수 있음)
        time.sleep(0.5)
        driver.close()
        time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화

def 로그인(srt_id, pw):
    global driver
    nextXpath('//*[@id="wrap"]/div[3]/div[1]/div/a[2]').click()
    nextXpath('//*[@id="srchDvNm01"]').send_keys(srt_id)
    nextXpath('/html/body/div[1]/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[1]/div[2]/input'
    ).send_keys(pw)
    nextXpath('//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input'
    ).click()

def 순차조회예약시도():
    print("1페이지 서칭")
    for i in range(1,100):
        try:
            print(checkTime(i).text)
            if checkTime(i).text == booking_time:
                for a in range(25):
                    target1 = booking(i)
                    if target1.text == "예약하기":
                        target1.click()
                        print("1순위 예약하였습니다. 시간 : {0}".format(datetime.datetime.now()))
                        Slack_Msg("1순위 예약에 성공하였습니다. 시간 : {0}".format(datetime.datetime.now()))
                        # break
                        return "예약성공"
                    else:
                        print(f"{a}번째 시도 - 매진 상태입니다. 시간 : {datetime.datetime.now()}")
                        print("리프레쉬")
                        time.sleep(1)
                        driver.refresh()
                        print("=" * 20)       
                break
        except:
            pass
    time.sleep(2)
    print("2페이지 이동")
    nextXpath('//*[@id="result-form"]/fieldset/div[8]/input').click()                 
    time.sleep(2)

    for i in range(1,100):
        try:  
            print(checkTime(i).text)
            if checkTime(i).text == booking_time:
                for a in range(25): 
                    target1 = booking(i)
                    print(target1.text)
                    if target1.text == "예약하기":
                        target1.click()
                        print("1순위 예약하였습니다. 시간 : {0}".format(datetime.datetime.now()))
                        Slack_Msg("1순위 예약에 성공하였습니다. 시간 : {0}".format(datetime.datetime.now()))
                        # break
                        return "예약성공"
                        
                    else:
                        print(f"{a}번째 시도 - 매진 상태입니다. 시간 : {datetime.datetime.now()}")
                        print("리프레쉬")
                        time.sleep(1)
                        driver.refresh()
                        print("=" * 20)
                break
        except:
            pass
    

###########
if __name__ == "__main__":

    for _ in range(50):
        service_obj = Service("./chromedriver/chromedriver.exe")
        driver = webdriver.Chrome(service=service_obj)
        url = 'https://etk.srail.kr/main.do'
        driver.get(url)
        팝업창닫고기본창활성화()

        로그인(srt_id, pw)
        time.sleep(1)
        팝업창닫고기본창활성화()

        nextXpath('//*[@id="dptRsStnCd"]').click()  #출발지 선택 버튼
        nextXpath(출발지).click()  #출발지 선택

        nextXpath('//*[@id="arvRsStnCd"]').click()  #도착지 선택 버튼
        nextXpath(도착지).click()  #도착지 선택
        nextXpath('//*[@id="search-form"]/fieldset/a').click()  # 간편조회하기 버튼

        nextXpath('//*[@id="dptDt"]').click()  # 날짜 조회 선택        
        select = Select(driver.find_element(By.NAME, 'dptDt')) # 날짜 보기 선택
        select.select_by_value(date)  # 희망날짜 선택

        nextXpath('//*[@id="search_top_tag"]/input').click() # 조회하기 버튼

        결과 = 순차조회예약시도()
        if 결과 == "예약성공":
            print("예약성공후 종료")
            break
        
        random_interval = random.randint(1, 3)
        time.sleep(random_interval)
        print(f"반복 랜덤 인터벌 {random_interval}")

    print("전체종료")
