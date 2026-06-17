from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from backend.services.room_service import create_room, get_room_by_id, update_room_name, is_owner, get_my_rooms, can_access_room, invite_member, get_my_pending_invites, accept_invite, reject_invite, leave_room, delete_room, get_room_members_with_names
from backend.decorators import login_required

# 방 관련 라우트 Blueprint
room_bp = Blueprint('room', __name__)

# 참여 중인 방 목록 조회
@room_bp.route('/rooms')
@login_required
def room_list():
    user_id = session.get('user_id')

    rooms = get_my_rooms(user_id)

    return render_template('room-list.html', rooms=rooms)

# 방 상세 정보 조회
@room_bp.route('/rooms/<room_id>')
@login_required
def detail(room_id):
    user_id = session.get('user_id')

    room = get_room_by_id(room_id)

    if not room:
        flash('존재하지 않는 방입니다.')
        return redirect(url_for('room.room_list'))

    if not can_access_room(room_id, user_id):
        flash('접근 권한이 없습니다.')
        return redirect(url_for('room.room_list'))

    members = get_room_members_with_names(room_id)
    return render_template('room-detail.html', room=room, members=members)

# 새로운 방 생성
@room_bp.route('/rooms/create', methods=['GET', 'POST'])
@login_required
def create():
    user_id = session.get('user_id')

    if request.method == 'POST':
        room_name = request.form.get('room_name', '').strip()

        if not room_name:
            flash('방 이름을 입력하세요.')
            return redirect(url_for('room.create'))

        room_id = create_room(room_name, user_id)

        flash('방이 생성되었습니다.')
        return redirect(url_for('room.detail', room_id=room_id))

    return render_template('create-room.html')

# 방 이름 변경
@room_bp.route('/rooms/<room_id>/edit-room-name', methods=['GET', 'POST'])
@login_required
def edit_room_name(room_id):
    user_id = session.get('user_id')

    if not is_owner(room_id, user_id):
        flash('방장만 방 이름을 변경할 수 있습니다.')
        return redirect(url_for('room.detail', room_id=room_id))

    if request.method == 'POST':
        new_name = request.form.get('room_name', '').strip()

        if not new_name:
            flash('방 이름을 입력하세요.')
            return redirect(url_for('room.edit_room_name', room_id=room_id))

        result = update_room_name(room_id, new_name)

        if result == 'NOT_EXIST_ROOM':
            flash('존재하지 않는 방입니다.')
            return redirect(url_for('room.room_list'))
        elif result == 'DB_FAIL':
            flash('방 이름 변경에 실패했습니다.')
            return redirect(url_for('room.detail', room_id=room_id))

        flash('방 이름이 변경되었습니다.')
        return redirect(url_for('room.detail', room_id=room_id))

    room = get_room_by_id(room_id)

    if not room:
        flash('존재하지 않는 방입니다.')
        return redirect(url_for('room.room_list'))

    return render_template('edit-room-name.html', room=room)

# 사용자를 방에 초대
@room_bp.route('/rooms/<room_id>/invite', methods=['GET', 'POST'])
@login_required
def invite(room_id):
    user_id = session.get('user_id')

    if not is_owner(room_id, user_id):
        flash('방장만 초대할 수 있습니다.')
        return redirect(url_for('room.detail', room_id=room_id))

    if request.method == 'POST':
        invite_username = request.form.get('invite_username', '').strip()

        if not invite_username:
            flash('사용자 이름을 입력하세요.')
            return redirect(url_for('room.invite', room_id=room_id))

        result = invite_member(room_id, user_id, invite_username)

        if result == 'NOT_EXIST_ROOM':
            flash('존재하지 않는 방입니다.')
            return redirect(url_for('room.room_list'))
        elif result == 'UNAUTHORIZED':
            flash('초대 권한이 없습니다.')
            return redirect(url_for('room.detail', room_id=room_id))
        elif result == 'NOT_EXIST_USER':
            flash('존재하지 않는 사용자입니다.')
            return redirect(url_for('room.detail', room_id=room_id))
        elif result == 'ALREADY_MEMBER':
            flash('이미 참여 중인 사용자입니다.')
            return redirect(url_for('room.detail', room_id=room_id))

        flash(f'{invite_username}님을 초대했습니다.')
        return redirect(url_for('room.detail', room_id=room_id))

    return render_template('invite-room.html', room_id=room_id)

# 사용자의 보류 중인 방 초대 목록 조회
@room_bp.route('/invites')
@login_required
def invite_list():
    user_id = session.get('user_id')

    invites = get_my_pending_invites(user_id)

    return render_template('invite-list.html', invites=invites)

# 방 초대 수락
@room_bp.route('/invites/<invite_id>/accept', methods=['POST'])
@login_required
def accept(invite_id):
    user_id = session.get('user_id')

    result = accept_invite(invite_id, user_id)

    if result == 'NOT_EXIST_INVITE':
        flash('존재하지 않는 초대입니다.')
        return redirect(url_for('room.invite_list'))
    elif result == 'UNAUTHORIZED':
        flash('초대 수락 권한이 없습니다.')
        return redirect(url_for('room.invite_list'))
    elif result == 'INVALID_INVITE_STATUS':
        flash('유효하지 않은 초대 상태입니다.')
        return redirect(url_for('room.invite_list'))

    flash('초대를 수락했습니다.')
    return redirect(url_for('room.room_list'))

# 방 초대 거절
@room_bp.route('/invites/<invite_id>/reject', methods=['POST'])
@login_required
def reject(invite_id):
    user_id = session.get('user_id')

    result = reject_invite(invite_id, user_id)

    if result == 'NOT_EXIST_INVITE':
        flash('존재하지 않는 초대입니다.')
        return redirect(url_for('room.invite_list'))
    elif result == 'UNAUTHORIZED':
        flash('초대 거절 권한이 없습니다.')
        return redirect(url_for('room.invite_list'))
    elif result == 'INVALID_INVITE_STATUS':
        flash('유효하지 않은 초대 상태입니다.')
        return redirect(url_for('room.invite_list'))

    flash('초대를 거절했습니다.')
    return redirect(url_for('room.invite_list'))

# 방에서 나가기
@room_bp.route('/rooms/<room_id>/leave', methods=['POST'])
@login_required
def leave(room_id):
    user_id = session.get('user_id')

    result = leave_room(room_id, user_id)

    if result == 'NOT_EXIST_ROOM':
        flash('존재하지 않는 방입니다.')
        return redirect(url_for('room.room_list'))
    elif result == 'OWNER_CANNOT_LEAVE':
        flash('방장은 방에서 나갈 수 없습니다.')
        return redirect(url_for('room.detail', room_id=room_id))
    elif result == 'DB_FAIL':
        flash('방에서 나가지 못했습니다.')
        return redirect(url_for('room.detail', room_id=room_id))

    flash('방에서 나갔습니다.')
    return redirect(url_for('room.room_list'))

# 방 삭제
@room_bp.route('/rooms/<room_id>/remove', methods=['POST'])
@login_required
def remove(room_id):
    user_id = session.get('user_id')

    result = delete_room(room_id, user_id)

    if result == 'NOT_EXIST_ROOM':
        flash('존재하지 않는 방입니다.')
        return redirect(url_for('room.room_list'))
    elif result == 'UNAUTHORIZED':
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('room.detail', room_id=room_id))
    elif result == 'DB_FAIL':
        flash('방 삭제에 실패했습니다.')
        return redirect(url_for('room.detail', room_id=room_id))

    flash('방이 삭제되었습니다.')
    return redirect(url_for('room.room_list'))