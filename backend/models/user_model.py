from flask import current_app
from bson.objectid import ObjectId

# 사용자 생성
def insert_user(user_data):
    return current_app.db.users.insert_one(user_data)

# ID로 사용자 조회
def find_user_by_id(user_id):
    return current_app.db.users.find_one({'_id': ObjectId(user_id)})

# username으로 사용자 조회
def find_user_by_username(username):
    return current_app.db.users.find_one({'username': username})

# 사용자 아이디 수정
def update_username_model(user_id, new_username):
    result = current_app.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'username': new_username}}
    )
    return result.matched_count > 0

# 비밀번호 수정
def update_password_model(user_id, hashed_password):
    result = current_app.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'password': hashed_password}}
    )
    return result.matched_count > 0

# 사용자 삭제
def delete_user_model(user_id):
    result = current_app.db.users.delete_one({'_id': ObjectId(user_id)})
    return result.deleted_count > 0