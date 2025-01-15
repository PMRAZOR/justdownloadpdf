'''
다운로드 성공 시:
다운로드 응답 코드: 200
PDF 다운로드 성공!

이러고 해당 py 파일 루트에 downloaded.pdf 파일 생성됨
'''

import requests
import urllib3
urllib3.disable_warnings()

session = requests.Session()

# localStroage에서 본인이 금방 발급받은 액세스 토큰 입력하기
# 엑세스 토큰 찾는법은 밑에 주석 참고
accessToken = "본인의_발급받은_엑세스토큰_입력"

# ex) 누군가의 만료된 project.ssafy.com 엑세스토큰
# accessToken = "ey~~8B"

# 기본 설정(파이어폭스 에뮬레이팅)
base_url = "https://project.ssafy.com"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Host': 'project.ssafy.com',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'Referer': 'https://project.ssafy.com/',
    'Origin': 'https://project.ssafy.com',
    # Bearer 인증
    'Authorization': f'Bearer {accessToken}'
}

'''
액세스 토큰은 Project.ssafy.com 로그인 이후 작업관리자에서 WEBDRM 프로세스를 끄면
project.ssafy.com의 접속은 끊기지만 세션과 엑세스 토큰은 볼 수 있음(초기화가 되지도 않음)
(이상황에서 새로고침 하면 자동으로 WEBDRM이 켜져고 다시 페이지를 로드해 토큰 초기화 안하고 추출이 가능함)

실제로 SSAFY 내의 서버엔 PDF파일이 MD5 해시로 암호화 되어있음
여기서 MD5로 암호화된 파일명을 알아내려면 실제로 SSAFY 내 뷰어에 접속해서 알아낼 방법밖에 없음
실제로 뷰어엔 WEBDRM이 걸려있어서 알아낼 수 없음
결국엔 PDF 파일명을 알아내려면 패킷을 캡쳐해서 알아낼 수 밖에 없음
와이어 샤크를 이용하면 패킷 캡쳐가 가능함
(물론 ssafy.com은 TLS로 암호화 되어있기때문에 sslkeylog로 복호화를 해줘야함)
(https://betterinvesting.tistory.com/287 복호화 세팅 참고용)

이제 와이어샤크에서 패킷캡처를 키고 project.ssafy.com 에서 자기가 받을 pdf를 전용 뷰어로 열면
캡처된 패킷에서 ssafy/api/file/download 를 검색하면 뒤에 MD5 해시로 암호화된 파일명을 찾을 수 있음

이 파일명을 믿의 코드에 넣으면 다운로드가 가능함
'''

try:
    # PDF 다운로드 시도 (파일명 MD5 해시화 되어있음)
    pdf_url = f"{base_url}/ssafy/api/file/download/subproject/MD5해시화된파일명/"
    # pdf_url = f"{base_url}/ssafy/api/file/download/subproject/8a81948994171cd101945d26ca51043c/"
    response = session.get(pdf_url, headers=headers, verify=False)
    
    print(f"다운로드 응답 코드: {response.status_code}")
    
    if response.status_code == 200:
        with open("downloaded.pdf", "wb") as f:
            f.write(response.content)
        print("PDF 다운로드 성공!")
    else:
        print("다운로드 실패")
        print("응답 헤더:", dict(response.headers))
        print("응답 내용:", response.text[:200])

except Exception as e:
    print(f"에러 발생: {str(e)}")

# 디버깅
# print("\n요청 정보:")
# print("헤더:", headers)