from bs4 import BeautifulSoup as bs4
from selenium import webdriver
import time

id = 'happine2s'
pwd = 'asdf1384/'
driver = webdriver.Chrome('/Users/bagsoyun/Downloads/chromedriver')
main = "https://ticket.interpark.com/Gate/TPLogin.asp?CPage=B&MN=Y&tid1=main_gnb&tid2=right_top&tid3=login&tid4=login"
musical = "http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=20001033"


def login():
    # 인터파크 홈페이지 접속하기
    driver.get(main)
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))

    # 로그인
    driver.find_element_by_id('userId').send_keys(id)
    driver.find_element_by_id('userPwd').send_keys(pwd)
    driver.find_element_by_id("btn_login").click()
    time.sleep(0.5)


def to_page():
    # 뮤지컬 예매 창 접속하기
    driver.get(musical)
    driver.execute_script('javascript:fnNormalBooking();')
    driver.switch_to.window(driver.window_handles[1])


def select_date():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.7)
    # 동적으로 바꾸기
    iframe = driver.find_element_by_id('ifrmBookStep')
    driver.switch_to.frame(iframe)

    # 날짜 선택하기
    driver.find_element_by_xpath('//*[@id="CellPlayDate"]').click()
    time.sleep(0.7)
    # 동적으로 바꾸기

    # 다음단계 넘어가기
    driver.switch_to.default_content()
    driver.execute_script("javascript:fnNextStep('P');")


def select_seat_2nd():
    while len(driver.find_elements_by_id('ifrmSeat')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeat'))
    while len(driver.find_elements_by_id('ifrmSeatDetail')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeatDetail'))
    time.sleep(0.7)

    # 좌석 2층, 3층으로 이동하기
    driver.execute_script("javascript:GetBlockSeatList('', '', 'RGN002')")


def select_seat_1st():
    driver.switch_to.window(driver.window_handles[1])
    while len(driver.find_elements_by_id('ifrmSeat')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeat'))
    while len(driver.find_elements_by_id('ifrmSeatDetail')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeatDetail'))
    # 동적으로 바꾸기
    time.sleep(0.7)

    # bs4로 1층 좌석 파싱하기
    req = driver.page_source
    dummy = bs4(req, 'html.parser')
    li = dummy.findAll('img', class_='stySeat')
    # 앞 좌석부터 선택하기

    # 1층에 잔여석이 없을 시 2층으로 넘어가기
    print(li)
    if (len(li) == 0):
        select_seat_2nd()
    else:
        pass

    seat = li[0]
    driver.execute_script(seat['onclick'] + ";")

    # 다음단계 넘어가기
    driver.switch_to.default_content()
    while len(driver.find_elements_by_id('ifrmSeat')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeat'))
    element = driver.find_element_by_xpath('//*[@id="NextStepImage"]')
    driver.execute_script("arguments[0].click();", element)


def ticket_num():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.3)
    iframe = driver.find_element_by_id('ifrmBookStep')
    driver.switch_to.frame(iframe)
    time.sleep(0.3)

    # selectbox 클릭
    select_box = driver.find_element_by_xpath('//*[@id="PriceRow001"]/td[3]/select')
    select_box.click()

    # selectbox안에 있는 요소 클릭
    t_num = select_box.find_element_by_xpath('//*[@id="PriceRow001"]/td[3]/select/option[2]')
    t_num.click()

    # 다음단계 넘어가기
    time.sleep(0.5)
    driver.switch_to.default_content()
    driver.execute_script("javascript:fnNextStep('P');")


def input_birth():
    iframe = driver.find_element_by_id('ifrmBookStep')
    driver.switch_to.frame(iframe)
    time.sleep(0.5)

    # 생일 입력하기
    birth = '030105'
    driver.find_element_by_id('YYMMDD').send_keys(birth)

    time.sleep(0.3)

    # 다음단계 넘어가기
    driver.switch_to.default_content()
    driver.execute_script("javascript:fnNextStep('P');")


def purchase():
    iframe = driver.find_element_by_id('ifrmBookStep')
    driver.switch_to.frame(iframe)
    time.sleep(1)

    # 무통장 입금 선택하기
    rad = driver.find_elements_by_xpath('//*[@id="Payment_22004"]/td/input')[0]
    rad.click()
    time.sleep(0.7)

    # 입금할 은행 선택하기
    driver.find_element_by_id('BankCode').click()
    bank = driver.find_element_by_xpath('//*[@id="BankCode"]/option[3]')
    bank.click()
    time.sleep(0.5)

    # 다음단계 넘어가기
    driver.switch_to.default_content()
    driver.execute_script("javascript:fnNextStep('P');")


def final_agree():
    iframe = driver.find_element_by_id('ifrmBookStep')
    driver.switch_to.frame(iframe)
    time.sleep(1)

    chk1 = driver.find_element_by_xpath('//*[@id="CancelAgree"]')
    chk1.click()
    chk2 = driver.find_element_by_xpath('//*[@id="CancelAgree2"]')
    chk2.click()
    time.sleep(0.5)

    # 다음단계 넘어가기
    driver.switch_to.default_content()
    driver.execute_script("javascript:fnNextStep('P');")


login()
to_page()
select_date()
select_seat_1st()
ticket_num()
input_birth()
purchase()
final_agree()
