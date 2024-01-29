# 필요 라이브러리 호출
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options        #자동꺼짐방지옵션 라이브러리
from datetime import datetime
import openpyxl  #엑셀활용위해 사용
import schedule #주기적실행을 위해 설정
import time #타임설정
import gspread  #구글스프레드시트 연동을 위한 라이브러리

# □■□■□■□■ 주기적으로 코드실행을 위한 변수
code_execution_cnt = 0
code_execution_max = 24  #24시간 기준으로 24지정

# □■□■□■□■ 함수정의
def action_start():
    # 전역변수 선언 및 회수출력
    global code_execution_cnt
    code_execution_cnt += 1
    print(f'{code_execution_cnt}회차 시작')  

    # 구글스프레드시트 연동을 위한 사용자 세팅
    my_gs_json = '/Users/kimsungwook/.json/racoon-test1-8eb04ba3c39c.json'
    gs_account_detail = gspread.service_account(my_gs_json) #사용자 계정 json 파일 사용 및 활성화
    main_gs_sheet = 'https://docs.google.com/spreadsheets/d/1i_ilm7ezmR7qh_PzjZBZjw7EfUH4Bezk77uZS22k7GQ/edit#gid=0' #구글 사용시트 주소
    useSheet = gs_account_detail.open_by_url(main_gs_sheet) #사용자 계정이 사용하고자하는 시트 url 설정
    print('구글 스프레드시트 연동 성공')

    # 엑셀파일 세팅
# =============================================================================
#     excel_data = openpyxl.Workbook() #엑셀파일 생성
#     excel_sheet = excel_data.active #데이터 적재 시트 지정 및 활성화
#     excel_sheet.column_dimensions['A'].width = 10   #엑셀 A열 너비 조정
#     excel_sheet.column_dimensions['B'].width = 10   #엑셀 B열 너비 조정
#     excel_sheet.column_dimensions['C'].width = 10   #엑셀 C열 너비 조정
#     excel_sheet.column_dimensions['D'].width = 10   #엑셀 D열 너비 조정
#     excel_sheet.column_dimensions['E'].width = 10   #엑셀 E열 너비 조정
#     excel_sheet.append(['오늘날짜', '시간대','판매건수','매출액','중간소계'])  #열별 1 행 필드명 지정
#     print('엑셀파일 세팅 완료')
# =============================================================================

    # 기본값 변수지정
    per_id = '3462901380'
    per_pw = '1234567890'
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_YMD = datetime.now().strftime('%Y-%m-%d')
    
    # 브라우저 자동 꺼짐옵션지정
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # 셀레니움옵션기능 활성화
    options = webdriver.ChromeOptions()
    options.add_argument("headless") # 창 숨기는 옵션 추가
    print('드라이버 실행 / 창옵션 숨김 완료')

    # 드라이버 변수 지정
    core_driver = webdriver.Chrome(options=options)

    # 접속 페이지 지정
    core_driver.get("https://www.orderqueen.kr/backoffice_admin/login.itp")

    # 입력 : 아이디(.find_element, .send_keys) / find_element 중 id의 값이 id인 부분을 찾고 값을 입력
    core_driver.find_element(by='id', value = 'userId').send_keys(per_id)
    # 입력: 비밀번호(.find_element, .send_keys) / find_element 중 id의 값이 pw인 부분을 찾고 값을 입력
    core_driver.find_element(by='id', value = 'pw').send_keys(per_pw)
    time.sleep(1)
    core_driver.find_element(by = 'id', value = 'btnLoginNew').click()
    print('계정/비번 입력완료')
    print('로그인 성공')
    print(f'현재 url 주소\t:\t{core_driver.current_url}')
    time.sleep(2)
    
    # 추출 : 데이터
    total_sale = core_driver.find_element(By.XPATH, value = '//*[@id="tbl-kiosk"]/tbody[2]/tr/td[2]').text
    print(f'{now} 누적매출액(당일기준)\t:\t{total_sale} 원')
    p = 0
    for v in range(1,25):
        time_zone = core_driver.find_element(By.XPATH, value = '//*[@id="tbl-time"]/tbody[1]/tr['+ str(v) + ']/td[1]').text
        sale_cnt =  core_driver.find_element(By.XPATH, value = '//*[@id="tbl-time"]/tbody[1]/tr['+ str(v) + ']/td[3]').text
        time_sale = core_driver.find_element(By.XPATH, value = '//*[@id="tbl-time"]/tbody[1]/tr[' + str(v) + ']/td[2]').text
        time_sale_int = int(time_sale.replace(',',''))
        p += time_sale_int
# =============================================================================
#         excel_sheet.append([now, time_zone, sale_cnt, time_sale, p])
# =============================================================================
        print(f'시간대 : {time_zone}\t 판매건수 : {sale_cnt}\t 매출액 : {time_sale} 원\t 소계 : {p} 원')
    print(f'{now} 데이터 갱신 완료 / 현시간까지 소계 : {p} 원')

    # 구글 엑셀시트 업데이트 
    my_sheet = useSheet.worksheet('일일 매출현황') #시트명과 동일하게 기재
    my_sheet.update('a1',total_sale)

# □■□■□■□■ 함수실행
# 1초에 한번씩 함수 실행 schedule.every(1).seconds.do(함수)
# 1분에 한번씩 함수 실행 schedule.every(1).minutes.do(함수)
# 2시간에 한번씩 함수 실행 schedule.every(1).hours.do(함수)

schedule.every(1).minutes.do(action_start)  # 1시간 마다 action_start 함수 실행

while True:
    schedule.run_pending()  # 함수 실행 메서드 .run_pending()
    if code_execution_cnt == code_execution_max:  # 코드 시행 회수가 24이상되면 실행 멈춤
        break
