from flask import Blueprint, render_template

# 메인 페이지 관련 라우트 Blueprint
main_bp = Blueprint('main', __name__)

# 홈페이지
@main_bp.route('/')
def home():
    return render_template('home.html')