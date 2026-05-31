from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime

from backend.models.user_model import insert_user, find_user_by_id, find_user_by_username, update_username_model, update_password_model, delete_user_model

# 회원가입 입력값 검증
def validate_register(username, email, password):
    if len(username) < 4:
        return 'USERNAME_SHORT'

    if len(password) < 8:
        return 'PASSWORD_SHORT'

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        return 'EMAIL_INVALID'

    return 'OK'

# 아이디 중복 확인 후 사용자 생성
def register_user(username, email, password):
    if find_user_by_username(username):
        return None

    hashed_pw = generate_password_hash(password)

    user_data = {
        'username': username,
        'email': email,
        'password': hashed_pw,
        'created_at': datetime.now()
    }

    insert_user(user_data)

    return find_user_by_username(username)

# 로그인 인증
def login_user(username, password):
    user = find_user_by_username(username)

    if not user:
        return None

    if not check_password_hash(user['password'], password):
        return None

    return user

# 아이디 변경
def update_username(user_id, new_username):
    if find_user_by_username(new_username):
        return 'DUPLICATE'

    success = update_username_model(user_id, new_username)

    if not success:
        return 'DB_FAIL'

    return 'SUCCESS'

# 비밀번호 변경
def update_password(user_id, old_password, new_password):
    user = find_user_by_id(user_id)

    if not check_password_hash(user['password'], old_password):
        return 'WRONG_OLD_PASSWORD'

    hashed_pw = generate_password_hash(new_password)

    success = update_password_model(user_id, hashed_pw)

    if not success:
        return 'DB_FAIL'

    return 'SUCCESS'

# 사용자 삭제 처리
def delete_user(user_id):
    return delete_user_model(user_id)