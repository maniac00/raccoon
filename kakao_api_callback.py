import requests
import json

url = 'https://kauth.kakao.com/oauth/token'
per_id = 'fb9b50df353ecef6fe844a17188b6bb3'  #키값
redirect_url = 'https://example.com/oauth'   #리다이렉트 url
code = 'aBGOz_dnKT_TYTOieez85h2zARJ0gtqcDlQDWJqDQ54JsIzky4cvsn4gYp8KPXVbAAABjURSfaWIenTzhLqDRQ'  #인증화면에서 받은 코드

data = {
    'grant_type' : 'authorization_code',
    'client_id' : per_id,
    'redirect_url' : redirect_url,
    'code' : code
}

#토큰 수신 및 덮어쓰기
response = requests.post(url, data=data)
tokens = response.json()

with open('token.json','w') as kakao: #토큰 만료시 다시 불러오면 덮어쓰기위해 작성
    json.dump(tokens, kakao)