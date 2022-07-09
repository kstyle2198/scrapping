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


print("SRT 예매 시도를 합니다.")
driver = webdriver.Chrome(executable_path="./chromedriver/chromedriver.exe")

# driver.maximize_window()  # 창 최대화
time.sleep(1)

## 열차표 예매 조건 설정
srt_id = get_secret("srt_id")
pw = get_secret("pw")
date = "10"

## SRT 홈피가서 로그인후 승차권 예매화면으로 이동
url = 'https://etk.srail.kr/main.do'
driver.get(url)
time.sleep(2)

# 팝업창 닫기
print("총 윈도우 개수 {0}".format(len(driver.window_handles)))
pop_up = len(driver.window_handles)

def nextXpath(path):
    return driver.find_element('xpath', path)

def nextLinkText(path):
    return driver.find_element('link text', path)

for i in range(pop_up - 1):
    print("{0}번째 팝업창 닫기".format(i + 1))
    driver.switch_to.window(
        driver.window_handles[1])  # 팝업창 선택후 닫기 (팝업창의 개수는 변경될 수 있음)
    time.sleep(0.5)
    driver.close()
    time.sleep(0.5)

time.sleep(1)
driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화
nextXpath('//*[@id="wrap"]/div[3]/div[1]/div/a[2]').click()
# driver.find_element("xpath",'//*[@id="wrap"]/div[3]/div[1]/div/a[2]').click()
# nextMove('//*[@id="wrap"]/div[3]/div[1]/div/a[2]').click()
time.sleep(1)

# 로그인
print("로그인 시작")
nextXpath('//*[@id="srchDvNm01"]').send_keys(srt_id)
nextXpath(
    '/html/body/div[1]/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[1]/div[2]/input'
).send_keys(pw)
nextXpath(
    '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input'
).click()
time.sleep(1)
print("로그인 종료후 팝업창 닫기")

print("총 윈도우 개수 {0}".format(len(driver.window_handles)))
pop_up2 = len(driver.window_handles)
for i in range(pop_up2 - 1):
    print("{0}번째 팝업창 닫기".format(i + 1))
    driver.switch_to.window(
        driver.window_handles[1])  # 팝업창 선택후 닫기 (팝업창의 개수는 변경될 수 있음)
    time.sleep(0.5)
    driver.close()
    time.sleep(0.5)

time.sleep(0.5)
driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화

print("출발역과 도착역 선택")

익산 = '//*[@id="dptRsStnCd"]/option[15]'
수서 = '//*[@id="arvRsStnCd"]/option[2]'
울산 = '//*[@id="dptRsStnCd"]/option[12]'

nextXpath('//*[@id="dptRsStnCd"]').click()  #출발지 선택 버튼
nextXpath(익산).click()  #출발지 선택

nextXpath('//*[@id="arvRsStnCd"]').click()  #도착지 선택 버튼
nextXpath(수서).click()  #도착지 선택

print("달력 및 날짜 선택")
nextXpath(
    '//*[@id="search-form"]/fieldset/div[3]/div/input[2]').click()  #달력버튼 클릭
time.sleep(1)
driver.switch_to.frame('_LAYER_BODY_')  # Inner HTML Iframe 이동 (달력 창)
time.sleep(1)
nextLinkText(date).click()
# driver.find_element_by_link_text(date).click()  # 예매 날짜 설정
time.sleep(2)

print("간편 조회버튼 클릭")
driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화

nextXpath(
    '//*[@id="search-form"]/fieldset/a').click()  # 간편조회하기 버튼
time.sleep(2)

print("2페이지 이동")
nextXpath('//*[@id="result-form"]/fieldset/div[8]/input'
                             ).click()  #다음화면(2페이지) 이동하기(14시경 이후)

time.sleep(2)

print("예매 루프 실행")

for i in range(1, 1000):
    print("{}번째 예약 시도".format(i))
    target1 = nextXpath(
        '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[5]/td[7]/a'
    )  # 19:10 열차
    print("1순위 현재 상태 : {}".format(target1.text))
    target2 = nextXpath(
        '//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[6]/td[7]/a'
    )  # 19:40 열차
    print("2순위 현재 상태 : {}".format(target2.text))

    if target1.text == "예약하기":
        target1.click()
        print("1순위 예약하였습니다. 시간 : {0}".format(datetime.datetime.now()))
        Slack_Msg("1순위 예약에 성공하였습니다. 시간 : {0}".format(datetime.datetime.now()))
        break
    # elif target2.text == "예약하기":
    #     target2.click()
    #     print("2순위 예약하였습니다. 시간 : {0}".format(datetime.datetime.now()))
    #     Slack_Msg("2순위 예약에 성공하였습니다. 시간 : {0}".format(datetime.datetime.now()))
    #     break
    else:
        print("매진 상태입니다. 시간 : {0}".format(datetime.datetime.now()))
        # Slack_Msg("매진 상태입니다. 시간 : {0}".format(datetime.datetime.now()))
        print("리프레쉬 시작")
        driver.refresh()
        time.sleep(1)
        print("리프레쉬 종료")
        print("=" * 20)

print("전체 작업 종료")

## 기타 참고
# WebDriverWait(driver, 10).until(EC.presence_of_element_located(By.XPATH, "~~~")) # 기본 대기시간 설정하되, 로딩 완료시 바로 실행하는 코드
# driver.execute_script("window.scrollTo(0, 1080)")  # 브라우저 높이인 1080 위치로 스크롤 내리기
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 화면 가장 아래로 스크롤 내리기
