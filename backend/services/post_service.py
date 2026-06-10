from bson.objectid import ObjectId
from datetime import datetime

from backend.services.room_service import is_member
from backend.services.emotion_service import analyze_emotion
from backend.models.room_model import find_room_by_id
from backend.models.post_model import insert_post, find_post_by_id, find_posts_by_room, update_post_model, delete_post_model

# 방 접근 검증
def validate_room_access(room_id, user_id):
    room = find_room_by_id(room_id)

    if not room:
        return 'NOT_EXIST_ROOM'

    if not is_member(room_id, user_id):
        return 'UNAUTHORIZED'

    return None

# 게시글 접근 검증
def validate_post_access(room_id, post_id):
    post = find_post_by_id(post_id)

    if not post:
        return 'NOT_EXIST_POST'

    if post['room_id'] != ObjectId(room_id):
        return 'INVALID_POST'

    return None

# 게시글 생성 및 감정 분석
def create_post(room_id, title, content, author_id, author_name):
    emotion = analyze_emotion(content)

    post_data = {
        'room_id': ObjectId(room_id),
        'title': title,
        'content': content,
        'author_id': ObjectId(author_id),
        'author_name': author_name,
        'emotion': emotion,
        'views': 0,
        'created_at': datetime.now(),
        'updated_at': None
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