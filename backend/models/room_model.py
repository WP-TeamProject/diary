from flask import current_app
from bson.objectid import ObjectId

# 방 생성
def insert_room(room_data):
    result = current_app.db.rooms.insert_one(room_data)
    return str(result.inserted_id)

# ID로 방 조회
def find_room_by_id(room_id):
    return current_app.db.rooms.find_one({'_id': ObjectId(room_id)})

# 전체 방 조회
def find_all_rooms():
    return list(current_app.db.rooms.find())

# 방 삭제
def delete_room_model(room_id):
    result = current_app.db.rooms.delete_one({'_id': ObjectId(room_id)})
    return result.deleted_count > 0