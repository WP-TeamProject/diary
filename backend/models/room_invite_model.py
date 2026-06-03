from flask import current_app
from bson.objectid import ObjectId

# 방 초대 생성
def insert_invite(invite_data):
    result = current_app.db.room_invites.insert_one(invite_data)
    return str(result.inserted_id)

# ID로 방 초대 조회
def find_invite_by_id(invite_id):
    return current_app.db.room_invites.find_one({'_id': ObjectId(invite_id)})

# 사용자 ID로 보류 중인 방 초대 조회
def find_pending_invites(user_id):
    return list(current_app.db.room_invites.find({
        'user_id': ObjectId(user_id),
        'status': 'pending'
    }))

# 특정 사용자의 특정 방에 대한 보류 중인 초대 조회
def find_pending_invite(room_id, user_id):
    return current_app.db.room_invites.find_one({
        'room_id': ObjectId(room_id),
        'user_id': ObjectId(user_id),
        'status': 'pending'
    })

# 방 초대 상태 업데이트
def update_invite_status(invite_id, new_status):
    result = current_app.db.room_invites.update_one(
        {'_id': ObjectId(invite_id)},
        {'$set': {'status': new_status}}
    )
    return result.matched_count > 0