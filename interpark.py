from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

id = 'happine2s'
pwd = 'psy3813!'
driver = webdriver.Chrome('/Users/bagsoyun/Downloads/chromedriver')
main = "https://ticket.interpark.com/Gate/TPLogin.asp?CPage=B&MN=Y&tid1=main_gnb&tid2=right_top&tid3=login&tid4=login"
musical = "http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=20001033"


def login():
    driver.get(main)
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element_by_id('userId').send_keys(id)
    driver.find_element_by_id('userPwd').send_keys(pwd)
    driver.find_element_by_id("btn_login").click()


def to_page():
    time.sleep(0.5)
    # 넘어가지 않으면 시간 늘리기
    driver.get(musical)
    driver.execute_script('javascript:fnNormalBooking();')


def select_date():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.7)
    #동적으로 바꾸기
    iframe = driver.find_element_by_id('ifrmBookStep')
    driver.switch_to.frame(iframe)
    driver.find_element_by_xpath('//*[@id="CellPlayDate"]').click()
    time.sleep(0.7)
    #동적으로 바꾸기
    driver.switch_to.default_content()
    driver.execute_script("javascript:fnNextStep('P');")


def select_seat():
    # 부모iframe
    while len(driver.find_elements_by_id('ifrmSeat')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeat'))

    # 자식iframe
    while len(driver.find_elements_by_id('ifrmSeatDetail')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeatDetail'))

    # 동적으로 바꾸기
    time.sleep(0.7)

    #bs4로 html 파싱하기
    req = driver.page_source
    dummy = bs4(req, 'html.parser')
    li = dummy.find_all('img')
    item = str(li[1])
    #seat = (etree.HTML(item)).xpath
    print(item)

    driver.switch_to.default_content()
    # 부모iframe
    while len(driver.find_elements_by_id('ifrmSeat')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeat'))

    #자바스크립트 실
    element = driver.find_element_by_xpath('//*[@id="NextStepImage"]')
    driver.execute_script("arguments[0].click();", element)


login()
to_page()
select_date()
select_seat()