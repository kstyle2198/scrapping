import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime
from slack import *
from config import get_secret


print("KTX 예매 시도를 합니다.")
driver = webdriver.Chrome(executable_path="./chromedriver/chromedriver.exe")
# driver.maximize_window()  # 창 최대화
time.sleep(3)
## 코레일 열차표 예매 조건 설정

ktx_id = get_secret("ktx_id")
pw = get_secret("pw")
depart = "익산"
arrive = "용산"
month = "2"
date = "3"
booking_time = "9"

## 코레일 홈피가서 로그인후 승차권 예매화면으로 이동
url = 'http://www.letskorail.com/'
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

time.sleep(1)
driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화
driver.find_element_by_xpath(
    '//*[@id="header"]/div[1]/div/ul/li[2]/a/img').click()
time.sleep(1)

print("로그인 시작")
driver.find_element_by_xpath('//*[@id="txtMember"]').send_keys(ktx_id)
driver.find_element_by_xpath(
    '/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[1]/form[1]/fieldset/div[1]/ul/li[2]/input'
).send_keys(pw)
driver.find_element_by_xpath('//*[@id="loginDisplay1"]/ul/li[3]/a/img').click()
time.sleep(5)

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

time.sleep(1)
driver.switch_to.window(driver.window_handles[0])  # 기본 창 선택 활성화
driver.find_element_by_xpath(
    '//*[@id="header"]/div[3]/div[1]/h3/a/img').click()
time.sleep(1)

print("승차권 조회후 예약 시도")
time.sleep(2)

## 예약 조건 입력
driver.find_element_by_xpath(
    '//*[@id="selGoTrainRa00"]').click()  # 조회대상 열차 종류 KTX/SRT 온리
driver.find_element_by_xpath('//*[@id="start"]').send_keys(
    Keys.BACKSPACE)  # 서울 기본값 지우기
driver.find_element_by_xpath('//*[@id="start"]').send_keys(
    Keys.BACKSPACE)  # 서울 기본값 지우기
driver.find_element_by_xpath('//*[@id="start"]').send_keys(depart)
driver.find_element_by_xpath('//*[@id="get"]').send_keys(
    Keys.BACKSPACE)  # 부산 기본값 지우기
driver.find_element_by_xpath('//*[@id="get"]').send_keys(
    Keys.BACKSPACE)  # 부산 기본값 지우기
driver.find_element_by_xpath('//*[@id="get"]').send_keys(arrive)
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="s_month"]').send_keys(month)
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="s_day"]').send_keys(date)
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="s_hour"]').send_keys(booking_time)
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="center"]/form/div/p/a/img').click()

## 조회후 열차 예매
print("일반실 예약시도")

## 예약 대상 변수에 담기 - tr[1]이면 조회 테이블상 첫번째, tr[2]이면 두번째 일반석 예약 대상임(여기서는 4개까지 설정 가능)
target1 = '//*[@id="tableResult"]/tbody/tr[1]/td[6]/a[1]/img'
target2 = '//*[@id="tableResult"]/tbody/tr[2]/td[6]/a[1]/img'
target3 = '//*[@id="tableResult"]/tbody/tr[3]/td[6]/a[1]/img'
target4 = '//*[@id="tableResult"]/tbody/tr[4]/td[6]/a[1]/img'

for i in range(1, 5):
    ## try & except로 순차적으로 4회 예약 시도
    print("{}차 시도".format(i))
    try:
        print("target1 예매 시도")
        driver.find_element_by_xpath(target1).click()
        Slack_Msg("승차권이 예약되었습니다. 시간 : {0}".format(
            datetime.datetime.now()))  # 예약 성공시 slack 문자 발송
        driver.find_element_by_xpath(target1).send_keys(Keys.ENTER)
        print("target1 예매 성공")
        sys.exit(1)

    except:
        try:
            print("target2 예매 시도")
            driver.find_element_by_xpath(target2).click()
            Slack_Msg("승차권이 예약되었습니다. 시간 : {0}".format(datetime.datetime.now()))
            driver.find_element_by_xpath(target2).send_keys(Keys.ENTER)
            print("target2 예매 성공")
            sys.exit(1)

        except:
            try:
                print("target3 예매 시도")
                driver.find_element_by_xpath(target3).click()
                Slack_Msg("승차권이 예약되었습니다. 시간 : {0}".format(
                    datetime.datetime.now()))
                driver.find_element_by_xpath(target3).send_keys(Keys.ENTER)
                print("target3 예매 성공")
                sys.exit(1)

            except:
                try:
                    print("target4 예매 시도")
                    driver.find_element_by_xpath(target4).click()
                    Slack_Msg("승차권이 예약되었습니다. 시간 : {0}".format(
                        datetime.datetime.now()))
                    driver.find_element_by_xpath(target4).send_keys(Keys.ENTER)
                    print("target4 예매 성공")
                    sys.exit(1)

                except:
                    time.sleep(1)
                    driver.refresh()
                    time.sleep(3)
                    print("리프레쉬 완료")
print("전체 작업 종료")
driver.close()
