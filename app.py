from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# 로컬호스트의 기본 포트인 27017 포트에서 실행 중인 MongoDB 서버에 연결하는 클라이언트 객체를 생성하여 client 변수에 할당
client = MongoClient('localhost', 27017)

db=client['test']

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)