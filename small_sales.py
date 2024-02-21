# 필요 라이브러리 호출
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options        #자동꺼짐방지옵션 라이브러리
from selenium.common.exceptions import NoSuchElementException    # 셀레니움 예외처리
from webdriver_manager.chrome import ChromeDriverManager
import time #타임설정
import gspread  #구글스프레드시트 연동을 위한 라이브러리
import sys
import logging
import logging.handlers

from rich.logging import RichHandler

warnings.filterwarnings(action='ignore')

LOG_PATH = "./log.log"
RICH_FORMAT = "[%(filename)s:%(lineno)s] >> %(message)s"
FILE_HANDLER_FORMAT = "[%(asctime)s]\\t%(levelname)s\\t[%(filename)s:%(funcName)s:%(lineno)s]\\t>> %(message)s"


def set_logger() -> logging.Logger:
    logging.basicConfig(
        level="INFO",
        format=RICH_FORMAT,
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    logger = logging.getLogger("rich")

    file_handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(FILE_HANDLER_FORMAT))
    logger.addHandler(file_handler)

    return logger

def handle_exception(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger("rich")

    logger.error("Unexpected exception",
                 exc_info=(exc_type, exc_value, exc_traceback))

# □■□■□■□■ 함수정의
def action_start():
    # 구글스프레드시트 연동을 위한 사용자 세팅
    try:       
        my_gs_json = '/Users/kimsungwook/raccoon/raccoon-2-f83f2a09096a.json'
        gs_account_detail = gspread.service_account(my_gs_json) #사용자 계정 json 파일 사용 및 활성화
        main_gs_sheet = 'https://docs.google.com/spreadsheets/d/1i_ilm7ezmR7qh_PzjZBZjw7EfUH4Bezk77uZS22k7GQ/edit#gid=0' #구글 사용시트 주소
        useSheet = gs_account_detail.open_by_url(main_gs_sheet) #사용자 계정이 사용하고자하는 시트 url 설정
    except gspread.exceptions.APIError:
        pass
    print('구글 스프레드시트 연동 성공')

    # 기본값 변수지정
    per_id = '3462901380'
    per_pw = '1234567890'
    # now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # now_YMD = datetime.now().strftime('%Y-%m-%d')
    
    # 브라우저 자동 꺼짐옵션지정
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(executable_path=ChromeDriverManager().install())


    # 셀레니움옵션기능 활성화
    options = webdriver.ChromeOptions()
    options.add_argument("headless") # 창 숨기는 옵션 추가
    print('드라이버 실행 / 창옵션 숨김 완료')

    # 드라이버 변수 지정
    core_driver = webdriver.Chrome(service=service, options=options)
    print('checkpoint-1')
    
    # 접속 페이지 지정
    core_driver.get("https://www.orderqueen.kr/backoffice_admin/login.itp")
    print('checkpoint-2')
    
    # 입력 : 아이디(.find_element, .send_keys) / find_element 중 id의 값이 id인 부분을 찾고 값을 입력
    core_driver.find_element(by='id', value = 'userId').send_keys(per_id)
    print('checkpoint-3')

    # 입력: 비밀번호(.find_element, .send_keys) / find_element 중 id의 값이 pw인 부분을 찾고 값을 입력
    core_driver.find_element(by='id', value = 'pw').send_keys(per_pw)
    time.sleep(1)
    core_driver.find_element(by = 'id', value = 'btnLoginNew').click()
    print('계정/비번 입력완료')
    print('로그인 성공')
    print(f'현재 url 주소\t:\t{core_driver.current_url}')
    time.sleep(5)
    
    # 추출 : 데이터
    try:
        total_sale = core_driver.find_element(By.XPATH, value = '//*[@id="tbl-kiosk"]/tbody[2]/tr/td[2]').text
    except (NoSuchElementException, UnboundLocalError):
        pass
        

    try:        
        my_sheet = useSheet.worksheet('일일 매출현황') #시트명과 동일하게 기재
        my_sheet.update('a1', [[total_sale]])
    except (NoSuchElementException, UnboundLocalError):
        pass


def main():
    logger = set_logger()
    sys.excepthook = handle_exception    
    action_start()

if __name__ == '__main__':
    
    main()
