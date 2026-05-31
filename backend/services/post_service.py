from bson.objectid import ObjectId
from datetime import datetime

from backend.services.emotion_service import analyze_emotion
from backend.models.user_model import find_user_by_id
from backend.models.post_model import insert_post, find_post_by_id, find_posts_by_room, update_post_model, delete_post_model

# 게시글 생성 및 감정 분석
def create_post(room_id, title, content, author_id, author_name):
    emotion = analyze_emotion(content)

    now = datetime.now()

    post_data = {
        'room_id': ObjectId(room_id),
        'title': title,
        'content': content,
        'author_id': ObjectId(author_id),
        'author_name': author_name,
        'emotion': emotion,
        'views': 0,
        'created_at': now,
        'updated_at': now
    }

    post_id = insert_post(post_data)

    return post_id

# 게시글 조회
def get_post_by_id(post_id):
    return find_post_by_id(post_id)

# 특정 방의 전체 게시글 조회
def get_posts_by_room(room_id):
    return find_posts_by_room(room_id)

# 게시글 수정 및 감정 재분석
def update_post(post_id, title, content):
    emotion = analyze_emotion(content)

    update_data = {
        'title': title,
        'content': content,
        'emotion': emotion,
        'updated_at': datetime.now()
    }

    return update_post_model(post_id, update_data)

# 게시글 삭제
def delete_post(post_id):
    return delete_post_model(post_id)