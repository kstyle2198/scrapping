# 크롬 주소창에 chrome://version 입력하면 크롬 버전 확인 가능

from selenium import webdriver

browser = webdriver.Chrome("./chromedriver/chromedriver.exe")
browser.get("http://naver.com")

'''
browser.find_element_by_class_name
browser.find_elements_by_link_text
browser.find_element_by_tag_name
browser.find_element_by_xpath
'''