import gspread
import sys

def main():
    # 구글 스프레드시트 환경 설정
    my_gs_json = '/root/raccoon/raccoon-2-f83f2a09096a.json'
    gs_account_detail = gspread.service_account(my_gs_json) #사용자 계정 json 파일 사용 및 활성화
    main_gs_sheet = 'https://docs.google.com/spreadsheets/d/1i_ilm7ezmR7qh_PzjZBZjw7EfUH4Bezk77uZS22k7GQ/edit#gid=0' #구글 사용시트 주소
    useSheet = gs_account_detail.open_by_url(main_gs_sheet) #사용자 계정이 사용하고자하는 시트 url 설정

    # 구글 스프레드시트에서 매출값 가져오기
    my_sheet = useSheet.worksheet('일일 매출현황') #시트명과 동일하게 기재
    value = my_sheet.acell('A1').value.replace(',','')+'원'
    with open("/root/raccoon/sales_now.txt", "w") as file:
        file.write(value)

if __name__ == "__main__":
    main()
