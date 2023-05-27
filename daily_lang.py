from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from slack import *

## 오늘 날짜 일본어 회화를 슬랙으로 보내주기

def get_lang():
    
    def web_wait(경로):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 경로)))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 경로)))
        except:
            print("에러")

    def nextXpath(path):
        web_wait(path)
        return driver.find_element('xpath', path)
    
    
    today = datetime.datetime.today().date()
    기준일 = datetime.date(2023, 5, 28)
    gap = today - 기준일
    today_num = 4523 + gap.days * 2
    Slack_Msg("==================")

    jp_url = 'https://audioclip.naver.com/channels/164/clips/'
    # cn_url = 'https://audioclip.naver.com/channels/165/clips/'

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
        nextXpath(
            '//*[@id="content"]/div/section/div[2]/div[1]/button[2]/span').click()

        title = nextXpath(
            '//*[@id="content"]/div/section/div[1]/div[2]/h3').text
        print(title)
        Slack_Msg(title)
        print("=" * 30)
        text = nextXpath(
            '//*[@id="chapter"]/div/ul/li[1]/p').text
        print(text)
        Slack_Msg(text)
        Slack_Msg(f"링크: {jp_url}+{today_num}")
        Slack_Msg("==================")

        driver.close()

        cn_add += 5  # 오늘자 회화 찾기 위한 날짜 조정 변수

    print("전체 작업 종료")
    
if __name__ == "__main__":
    get_lang()