import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Firebase 인증 및 초기화
cred = credentials.Certificate("koribor-chart-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://koribor-chart-default-rtdb.firebaseio.com/koribor/'
})

def get_koribor_rate():
    # 예시 URL (실제 Koribor 금리 페이지로 교체)
    url = 'https://koribor.kr/rates'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 페이지에서 금리 정보를 추출하는 코드 (실제 웹사이트의 구조에 맞게 변경)
    rate_element = soup.find('div', {'class': 'rate-value'})
    rate = rate_element.text.strip() if rate_element else None
    
    return rate

def save_to_firebase(rate):
    # Firebase 데이터베이스에 저장
    now = datetime.now().strftime('%Y-%m-%d')
    ref = db.reference(f'koribor-rates/{now}')
    ref.set({
        'date': now,
        'rate': rate
    })

if __name__ == "__main__":
    rate = get_koribor_rate()
    if rate:
        save_to_firebase(rate)
        print(f"Koribor rate {rate} saved successfully.")
    else:
        print("Failed to retrieve Koribor rate.")
