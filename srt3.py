from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
import time
import datetime
import random
from slack import Slack_Msg
from config import get_secret

# Configuration
SRT_ID = get_secret("srt_id")
SRT_PW = get_secret("srt_pw")
DATE = "20250203"
BOOKING_TIME = "05:51"
DEPARTURE_STATION = '익산'
ARRIVAL_STATION = '수서'

# XPaths
DEPARTURE_XPATH = f'//*[@id="dptRsStnCd"]/option[text()="{DEPARTURE_STATION}"]'
ARRIVAL_XPATH = f'//*[@id="arvRsStnCd"]/option[text()="{ARRIVAL_STATION}"]'

def initialize_driver():
    service_obj = Service("./chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service_obj)
    return driver

def close_popups_and_switch_to_main_window(driver):
    pop_up_count = len(driver.window_handles)
    print(f"Total windows: {pop_up_count}")
    time.sleep(0.5)

    for i in range(pop_up_count - 1):
        print(f"Closing popup window {i + 1}")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)
        driver.close()
        time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[0])

def login(driver, srt_id, srt_pw):
    driver.find_element(By.XPATH, '//*[@id="wrap"]/div[3]/div[1]/div/a[2]').click()
    driver.find_element(By.XPATH, '//*[@id="srchDvNm01"]').send_keys(srt_id)
    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[1]/div[2]/input').send_keys(srt_pw)
    driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()

def search_trains(driver):
    driver.find_element(By.XPATH, '//*[@id="dptRsStnCd"]').click()
    driver.find_element(By.XPATH, DEPARTURE_XPATH).click()
    driver.find_element(By.XPATH, '//*[@id="arvRsStnCd"]').click()
    driver.find_element(By.XPATH, ARRIVAL_XPATH).click()
    driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/a').click()
    time.sleep(2)
    select = Select(driver.find_element(By.NAME, 'dptDt'))
    select.select_by_value(DATE)
    driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input').click()
    time.sleep(2)

def attempt_booking(driver):
    print("Searching on page 1")
    for i in range(1, 100):
        try:
            time_element = driver.find_element(By.XPATH, f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{i}]/td[4]/em')
            if time_element.text == BOOKING_TIME:
                for attempt in range(25):
                    booking_element = driver.find_element(By.XPATH, f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a/span')
                    if booking_element.text == "예약하기":
                        booking_element.click()
                        print(f"Successfully booked at {datetime.datetime.now()} : from {DEPARTURE_STATION} to {ARRIVAL_STATION} at {BOOKING_TIME} on {DATE}")
                        Slack_Msg(f"Successfully booked at {datetime.datetime.now()} : from {DEPARTURE_STATION} to {ARRIVAL_STATION} at {BOOKING_TIME} on {DATE}")
                        return "Booking Success"
                    else:
                        print(f"Attempt {attempt}: Sold out at {datetime.datetime.now()} : from {DEPARTURE_STATION} to {ARRIVAL_STATION} at {BOOKING_TIME} on {DATE}")
                        time.sleep(1)
                        driver.refresh()
                break
        except Exception as e:
            print(f"Error: {e}")
            continue

        print("Moving to page 2")
        driver.find_element(By.XPATH, '//*[@id="result-form"]/fieldset/div[8]/input').click()
        for i in range(1, 100):
            try:
                time_element = driver.find_element(By.XPATH, f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{i}]/td[4]/em')
                if time_element.text == BOOKING_TIME:
                    for attempt in range(25):
                        booking_element = driver.find_element(By.XPATH, f'//*[@id="result-form"]/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a/span')
                        if booking_element.text == "예약하기":
                            booking_element.click()
                            print(f"Successfully booked at {datetime.datetime.now()} : from {DEPARTURE_STATION} to {ARRIVAL_STATION} at {BOOKING_TIME} on {DATE}")
                            Slack_Msg(f"Successfully booked at {datetime.datetime.now()} : from {DEPARTURE_STATION} to {ARRIVAL_STATION} at {BOOKING_TIME} on {DATE}")
                            return "Booking Success"
                        else:
                            print(f"Attempt {attempt}: Sold out at {datetime.datetime.now()} : from {DEPARTURE_STATION} to {ARRIVAL_STATION} at {BOOKING_TIME} on {DATE}")
                            time.sleep(1)
                            driver.refresh()
                    break
            except Exception as e:
                print(f"Error: {e}")
                continue

    return "Booking Failed"

def main():
    for _ in range(50):
        driver = initialize_driver()
        driver.get('https://etk.srail.kr/main.do')
        close_popups_and_switch_to_main_window(driver)

        login(driver, SRT_ID, SRT_PW)
        time.sleep(2)
        close_popups_and_switch_to_main_window(driver)

        search_trains(driver)
        result = attempt_booking(driver)

        if result == "Booking Success":
            print("Booking successful, exiting...")
            break

        driver.close()

        random_interval = random.randint(1, 3)
        time.sleep(random_interval)
        print(f"Random interval: {random_interval} seconds")

    print("Script ended")

if __name__ == "__main__":
    main()