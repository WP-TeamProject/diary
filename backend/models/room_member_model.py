from flask import current_app
from bson.objectid import ObjectId

# 방 참여자 추가
def add_member(member_data):
    result = current_app.db.room_members.insert_one(member_data)
    return str(result.inserted_id)

# 특정 사용자의 방 참여 정보 조회
def find_member(room_id, user_id):
    return current_app.db.room_members.find_one({
        'room_id': ObjectId(room_id),
        'user_id': ObjectId(user_id)
    })

# 방 참여자 목록 조회
def find_members_by_room(room_id):
    return list(current_app.db.room_members.find({'room_id': ObjectId(room_id)}))

# 사용자가 참여 중인 방 목록 조회
def find_rooms_by_user(user_id):
    return list(current_app.db.room_members.find({'user_id': ObjectId(user_id)}))

# 방에서 사용자 제거
def remove_member(room_id, user_id):
    result = current_app.db.room_members.delete_one({
        'room_id': ObjectId(room_id),
        'user_id': ObjectId(user_id)
    })
    return result.deleted_count > 0

# 방의 모든 참여자 제거
def delete_members_by_room(room_id):
    result = current_app.db.room_members.delete_many({'room_id': ObjectId(room_id)})
    return result.deleted_count > 0