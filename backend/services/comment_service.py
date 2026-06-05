from bson.objectid import ObjectId
from datetime import datetime

from backend.models.comment_model import insert_comment, find_comment_by_id, find_comments_by_post, update_comment_model, delete_comment_model

# 댓글 생성
def create_comment(post_id, content, author_id, author_name):
    comment_data = {
        'post_id': ObjectId(post_id),
        'content': content,
        'author_id': ObjectId(author_id),
        'author_name': author_name,
        'created_at': datetime.now(),
        'updated_at': None
    }

    comment_id = insert_comment(comment_data)

    return comment_id

# 댓글 조회
def get_comment_by_id(comment_id):
    return find_comment_by_id(comment_id)

# 특정 게시글의 댓글 목록 조회
def get_comments_by_post(post_id):
    return find_comments_by_post(post_id)

# 댓글 수정
def update_comment(comment_id, content):
    update_data = {
        'content': content,
        'updated_at': datetime.now()
    }

    return update_comment_model(comment_id, update_data)

# 댓글 삭제
def delete_comment(comment_id):
    return delete_comment_model(comment_id)