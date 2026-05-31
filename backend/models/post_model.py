from flask import current_app
from bson.objectid import ObjectId

# 게시글 생성
def insert_post(post_data):
    result = current_app.db.posts.insert_one(post_data)
    return str(result.inserted_id)

# ID로 게시글 조회
def find_post_by_id(post_id):
    return current_app.db.posts.find_one({'_id': ObjectId(post_id)})

# 특정 방의 최신순 게시글 목록 조회
def find_posts_by_room(room_id):
    return list(current_app.db.posts.find({'room_id': ObjectId(room_id)}).sort('created_at', -1))

# 조회수 증가
def increase_views(post_id):
    current_app.db.posts.update_one(
        {'_id': ObjectId(post_id)},
        {'$inc': {'views': 1}}
    )

# 게시글 수정
def update_post_model(post_id, update_data):
    result = current_app.db.posts.update_one(
        {'_id': ObjectId(post_id)},
        {'$set': update_data}
    )
    return result.matched_count > 0

# 게시글 삭제
def delete_post_model(post_id):
    result = current_app.db.posts.delete_one({'_id': ObjectId(post_id)})
    return result.deleted_count > 0