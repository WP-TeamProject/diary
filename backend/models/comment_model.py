from flask import current_app
from bson.objectid import ObjectId

# 댓글 생성
def insert_comment(comment_data):
    result = current_app.db.comments.insert_one(comment_data)
    return str(result.inserted_id)

# ID로 댓글 조회
def find_comment_by_id(comment_id):
    return current_app.db.comments.find_one({'_id': ObjectId(comment_id)})

# 특정 게시글의 댓글 목록 조회
def find_comments_by_post(post_id):
    return list(current_app.db.comments.find({'post_id': ObjectId(post_id)}).sort('created_at', 1))

# 댓글 수정
def update_comment_model(comment_id, update_data):
    result = current_app.db.comments.update_one(
        {'_id': ObjectId(comment_id)},
        {'$set': update_data}
    )
    return result.matched_count > 0

# 댓글 삭제
def delete_comment_model(comment_id):
    result = current_app.db.comments.delete_one({'_id': ObjectId(comment_id)})
    return result.deleted_count > 0