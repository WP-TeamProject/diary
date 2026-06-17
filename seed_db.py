import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
ATLAS_URI = os.getenv('MONGO_URI')

client = MongoClient(ATLAS_URI)
db = client['diary']

def seed_users():
    print("🌱 테스트용 유저 계정 심기...")

    # 공통 테스트 비밀번호: 1234
    test_password = generate_password_hash('1234')

    # 생성할 유저 목록 리스트
    users_to_create = [
        {
            "username": "master",
            "email": "master@diary.com",
            "password": test_password,
            "role": "admin", # 관리자
            "created_at": datetime.utcnow()
        },
        {
            "username": "test1",
            "email": "test1@diary.com",
            "password": test_password,
            "role": "user",
            "created_at": datetime.utcnow()
        },
        {
            "username": "test2",
            "email": "test2@diary.com",
            "password": test_password,
            "role": "user",
            "created_at": datetime.utcnow()
        },
        {
            "username": "test3",
            "email": "test3@diary.com",
            "password": test_password,
            "role": "user",
            "created_at": datetime.utcnow()
        }
    ]

    count = 0
    for user_data in users_to_create:
        if not db.users.find_one({'username': user_data['username']}):
            db.users.insert_one(user_data)
            print(f"✅ 유저 생성 완료: {user_data['username']}")
            count += 1
        else:
            print(f"⚠️ 이미 존재하는 유저: {user_data['username']}")

    print(f"🎉 총 {count}명의 테스트 유저가 DB에 성공적으로 주입 완료")
    print("👉 아이디 'master', 비밀번호 '1234'")

if __name__ == '__main__':
    seed_users()