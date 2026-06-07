from bson.objectid import ObjectId
from datetime import datetime

from backend.models.user_model import find_user_by_username
from backend.models.room_model import insert_room, find_room_by_id, update_room_name_model, delete_room_model
from backend.models.room_member_model import add_member, find_member, find_members_by_room, find_rooms_by_user, remove_member, delete_members_by_room
from backend.models.room_invite_model import insert_invite, find_invite_by_id, find_pending_invites, find_pending_invite, update_invite_status

# 새로운 방 생성
def create_room(name, owner_id):
    room_data = {
        'room_name': name,
        'owner_id': ObjectId(owner_id),
        'created_at': datetime.now()
    }

    room_id = insert_room(room_data)

    member_data = {
        'room_id': ObjectId(room_id),
        'user_id': ObjectId(owner_id),
        'joined_at': datetime.now()
    }

    add_member(member_data)

    return room_id

# 방 조회
def get_room_by_id(room_id):
    return find_room_by_id(room_id)

# 방 이름 변경
def update_room_name(room_id, new_name):
    room = find_room_by_id(room_id)

    if not room:
        return 'NOT_EXIST_ROOM'

    success = update_room_name_model(room_id, new_name)

    if not success:
        return 'DB_FAIL'

    return 'SUCCESS'

# 방장 여부 확인
def is_owner(room_id, user_id):
    room = find_room_by_id(room_id)
    return room and room['owner_id'] == ObjectId(user_id)

# 방 참여 여부 확인
def is_member(room_id, user_id):
    member = find_member(room_id, user_id)
    return member is not None

# 방 참여자 목록 조회
def get_room_members(room_id):
    return find_members_by_room(room_id)

# 사용자가 참여 중인 방 목록 조회
def get_my_rooms(user_id):
    memberships = find_rooms_by_user(user_id)

    rooms = []

    for membership in memberships:
        room = find_room_by_id(membership['room_id'])

        if room:
            rooms.append(room)

    return rooms

# 방 접근 권한 확인
def can_access_room(room_id, user_id):
    room = find_room_by_id(room_id)

    if not room:
        return False

    return is_member(room_id, user_id)

# 사용자를 방에 초대
def invite_member(room_id, owner_id, username):
    room = find_room_by_id(room_id)

    if not room:
        return 'NOT_EXIST_ROOM'

    if room['owner_id'] != ObjectId(owner_id):
        return 'UNAUTHORIZED'

    invite_user = find_user_by_username(username)

    if not invite_user:
        return 'NOT_EXIST_USER'

    invite_user_id = str(invite_user['_id'])

    if is_member(room_id, invite_user_id):
        return 'ALREADY_MEMBER'
    
    if find_pending_invite(room_id, invite_user_id):
        return 'ALREADY_INVITED'

    invite_data = {
        'room_id': ObjectId(room_id),
        'user_id': ObjectId(invite_user_id),
        'status': 'pending',
        'invited_at': datetime.now()
    }

    insert_invite(invite_data)

    return 'SUCCESS'

# 사용자의 보류 중인 방 초대 조회
def get_my_pending_invites(user_id):
    return find_pending_invites(user_id)

# 방 초대 수락
def accept_invite(invite_id, user_id):
    invite = find_invite_by_id(invite_id)

    if not invite:
        return 'NOT_EXIST_INVITE'

    if invite['user_id'] != ObjectId(user_id):
        return 'UNAUTHORIZED'

    if invite['status'] != 'pending':
        return 'INVALID_INVITE_STATUS'

    room_id = str(invite['room_id'])
    user_id = str(invite['user_id'])

    member_data = {
        'room_id': ObjectId(room_id),
        'user_id': ObjectId(user_id),
        'joined_at': datetime.now()
    }

    add_member(member_data)

    update_invite_status(invite_id, 'accepted')

    return 'SUCCESS'

# 방 초대 거절
def reject_invite(invite_id, user_id):
    invite = find_invite_by_id(invite_id)

    if not invite:
        return 'NOT_EXIST_INVITE'

    if invite['user_id'] != ObjectId(user_id):
        return 'UNAUTHORIZED'

    if invite['status'] != 'pending':
        return 'INVALID_INVITE_STATUS'

    update_invite_status(invite_id, 'rejected')

    return 'SUCCESS'

# 방에서 나가기
def leave_room(room_id, user_id):
    room = find_room_by_id(room_id)

    if not room:
        return 'NOT_EXIST_ROOM'

    if room['owner_id'] == ObjectId(user_id):
        return 'OWNER_CANNOT_LEAVE'

    if not remove_member(room_id, user_id):
        return 'DB_FAIL'

    return 'SUCCESS'

# 방 삭제
def delete_room(room_id, user_id):
    room = find_room_by_id(room_id)

    if not room:
        return 'NOT_EXIST_ROOM'

    if room['owner_id'] != ObjectId(user_id):
        return 'UNAUTHORIZED'

    # 참여자 정보 삭제
    if not delete_members_by_room(room_id):
        return 'DB_FAIL'

    # 방 정보 삭제
    if not delete_room_model(room_id):
        return 'DB_FAIL'

    return 'SUCCESS'