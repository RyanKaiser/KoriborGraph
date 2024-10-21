import csv
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Firebase 인증 및 초기화
cred = credentials.Certificate("koribor-chart-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://koribor-chart-default-rtdb.firebaseio.com/koribor/'
})


# CSV 파일 경로
csv_file_path = 'koribor_2014_202410.csv'

# 데이터를 Firebase에 업로드하는 함수
def upload_to_firebase(data):
    for index, row in data.iterrows():
        date = row['Date']
        rates = {
            '1Week': row['1Week'],
            '1Month': row['1Month'],
            '2Month': row['2Month'],
            '3Month': row['3Month'],
            '6Month': row['6Month'],
            '12Month': row['12Month'],
        }
        ref = db.reference(f'koribor-rates/{date}')
        ref.set(rates)

# CSV 파일 파싱 및 Firebase 업로드
def process_csv_and_upload(file_path):
    df = pd.read_csv(file_path)
    df = df.drop(0)  # 첫 번째 행 제거 (열 이름이 중복되어 있음)
    upload_to_firebase(df)

# CSV 파일 처리 및 Firebase 업로드 실행
process_csv_and_upload(csv_file_path)