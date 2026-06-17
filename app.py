import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

from backend.routes.main_routes import main_bp
from backend.routes.user_routes import user_bp
from backend.routes.room_routes import room_bp
from backend.routes.post_routes import post_bp

load_dotenv()

app = Flask(__name__)

# 세션 보안 키
app.secret_key = os.getenv('SECRET_KEY')

ATLAS_URI = os.getenv('MONGO_URI')

# MongoDB 연결
client = MongoClient(ATLAS_URI)
app.db = client['diary']

# Blueprint 등록
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(room_bp)
app.register_blueprint(post_bp)

if __name__ == '__main__':
    app.run(debug=True)