from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from backend.services.user_service import validate_register, register_user, login_user, update_username, update_password, delete_user
from backend.decorators import login_required

# 사용자 관련 라우트 Blueprint
user_bp = Blueprint('user', __name__)

# 회원가입
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not email or not password:
            flash('모든 값을 입력해주세요.')
            return redirect(url_for('user.register'))

        result = validate_register(username, email, password)

        if result == 'USERNAME_SHORT':
            flash('아이디는 4자 이상이어야 합니다.')
            return redirect(url_for('user.register'))

        if result == 'PASSWORD_SHORT':
            flash('비밀번호는 8자 이상이어야 합니다.')
            return redirect(url_for('user.register'))

        if result == 'EMAIL_INVALID':
            flash('이메일 형식이 올바르지 않습니다.')
            return redirect(url_for('user.register'))

        user = register_user(username, email, password)

        if not user:
            flash('이미 존재하는 아이디입니다.')
            return redirect(url_for('user.register'))

        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('user.login'))

    return render_template('register.html')

# 로그인
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = login_user(username, password)

        if not user:
            flash('아이디 또는 비밀번호가 올바르지 않습니다.')
            return redirect(url_for('user.login'))

        # 로그인 세션 저장
        session['user_id'] = str(user['_id'])
        session['username'] = user['username']

        flash('로그인되었습니다.')
        return redirect(url_for('main.home'))

    return render_template('login.html')

# 로그아웃
@user_bp.route('/logout')
def logout():
    session.clear()
    flash('로그아웃되었습니다.')
    return redirect(url_for('main.home'))

# 아이디 변경
@user_bp.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    user_id = session.get('user_id')

    if request.method == 'POST':
        new_username = request.form.get('username', '').strip()

        if not new_username:
            flash('아이디를 입력하세요.')
            return redirect(url_for('user.change_username'))

        result = update_username(user_id, new_username)

        if result == 'DUPLICATE':
            flash('이미 존재하는 아이디입니다.')
            return redirect(url_for('user.change_username'))
        elif result == 'DB_FAIL':
            flash('아이디 변경에 실패했습니다.')
            return redirect(url_for('user.change_username'))

        session['username'] = new_username

        flash('아이디가 변경되었습니다.')
        return redirect(url_for('main.home'))

    return render_template('change-username.html')

# 비밀번호 변경
@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user_id = session.get('user_id')

    if request.method == 'POST':
        old_password = request.form.get('old_password', '').strip()
        new_password = request.form.get('new_password', '').strip()

        if not old_password or not new_password:
            flash('모든 값을 입력해주세요.')
            return redirect(url_for('user.change_password'))

        if len(new_password) < 8:
            flash('비밀번호는 8자 이상이어야 합니다.')
            return redirect(url_for('user.change_password'))

        result = update_password(user_id, old_password, new_password)

        if result == 'WRONG_OLD_PASSWORD':
            flash('현재 비밀번호가 올바르지 않습니다.')
            return redirect(url_for('user.change_password'))
        elif result == 'DB_FAIL':
            flash('비밀번호 변경에 실패했습니다.')
            return redirect(url_for('user.change_password'))

        flash('비밀번호가 변경되었습니다.')
        return redirect(url_for('main.home'))

    return render_template('change-password.html')

# 회원탈퇴
@user_bp.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    user_id = session.get('user_id')

    success = delete_user(user_id)

    if not success:
        flash('회원탈퇴에 실패했습니다.')
        return redirect(url_for('main.home'))

    session.clear()
    flash('회원탈퇴가 완료되었습니다.')
    return redirect(url_for('main.home'))