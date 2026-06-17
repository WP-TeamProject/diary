from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from bson.objectid import ObjectId

from backend.services.post_service import validate_room_access, validate_post_access, create_post, get_post_by_id, get_posts_by_room, update_post, delete_post
from backend.services.comment_service import create_comment, get_comment_by_id, get_comments_by_post, update_comment, delete_comment
from backend.models.post_model import increase_views
from backend.decorators import login_required

# 게시글 관련 라우트 Blueprint
post_bp = Blueprint('post', __name__)

# 게시글 목록
@post_bp.route('/rooms/<room_id>/posts')
@login_required
def post_list(room_id):
    user_id = session.get('user_id')

    room_error = validate_room_access(room_id, user_id)

    if room_error == 'NOT_EXIST_ROOM':
        flash('존재하지 않는 방입니다.')
    elif room_error == 'UNAUTHORIZED':
        flash('접근 권한이 없습니다.')

    if room_error:
        return redirect(url_for('main.home'))

    posts = get_posts_by_room(room_id)
    return render_template('post-list.html', posts=posts)

# 게시글 상세 조회
@post_bp.route('/rooms/<room_id>/posts/<post_id>')
@login_required
def detail(room_id, post_id):
    user_id = session.get('user_id')

    room_error = validate_room_access(room_id, user_id)

    if room_error == 'NOT_EXIST_ROOM':
        flash('존재하지 않는 방입니다.')
    elif room_error == 'UNAUTHORIZED':
        flash('접근 권한이 없습니다.')

    if room_error:
        return redirect(url_for('main.home'))

    post_error = validate_post_access(room_id, post_id)

    if post_error == 'NOT_EXIST_POST':
        flash('게시글이 존재하지 않습니다.')
    elif post_error == 'INVALID_POST':
        flash('잘못된 접근입니다.')

    if post_error:
        return redirect(url_for('post.post_list', room_id=room_id))

    post = get_post_by_id(post_id)

    increase_views(post_id)

    comments = get_comments_by_post(post_id)

    if str(post['author_id']) != str(user_id):
        # 프라이빗 텍스트 처리 원문은 자신만 확인 가능
        post['content'] = "🔒 작성자 본인만 원문을 확인할 수 있어요."

    return render_template('post-detail.html', post=post, comments=comments)

# 게시글 작성
@post_bp.route('/rooms/<room_id>/posts/write', methods=['GET', 'POST'])
@login_required
def write(room_id):
    user_id = session.get('user_id')

    room_error = validate_room_access(room_id, user_id)

    if room_error == 'NOT_EXIST_ROOM':
        flash('존재하지 않는 방입니다.')
    elif room_error == 'UNAUTHORIZED':
        flash('접근 권한이 없습니다.')

    if room_error:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash('제목과 내용을 입력하세요.')
            return redirect(url_for('post.write', room_id=room_id))

        # 작성자 정보는 세션에서 가져옴
        author_id = user_id
        author_name = session['username']

        post_id = create_post(room_id, title, content, author_id, author_name)

        flash('게시글이 작성되었습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    return render_template('write-post.html', room_id=room_id)

# 게시글 수정
@post_bp.route('/rooms/<room_id>/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(room_id, post_id):
    user_id = session.get('user_id')

    room_error = validate_room_access(room_id, user_id)

    if room_error == 'NOT_EXIST_ROOM':
        flash('존재하지 않는 방입니다.')
    elif room_error == 'UNAUTHORIZED':
        flash('접근 권한이 없습니다.')

    if room_error:
        return redirect(url_for('main.home'))

    post_error = validate_post_access(room_id, post_id)

    if post_error == 'NOT_EXIST_POST':
        flash('게시글이 존재하지 않습니다.')
    elif post_error == 'INVALID_POST':
        flash('잘못된 접근입니다.')

    if post_error:
        return redirect(url_for('post.post_list', room_id=room_id))

    post = get_post_by_id(post_id)

    if post['author_id'] != ObjectId(user_id):
        flash('수정 권한이 없습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash('제목과 내용을 입력하세요.')
            return redirect(url_for('post.edit', room_id=room_id, post_id=post_id))

        success = update_post(post_id, title, content)

        if not success:
            flash('게시글 수정에 실패했습니다.')
            return redirect(url_for('post.edit', room_id=room_id, post_id=post_id))

        flash('게시글이 수정되었습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    return render_template('edit-post.html', post=post)

# 게시글 삭제
@post_bp.route('/rooms/<room_id>/posts/<post_id>/remove', methods=['POST'])
@login_required
def remove(room_id, post_id):
    user_id = session.get('user_id')

    room_error = validate_room_access(room_id, user_id)

    if room_error == 'NOT_EXIST_ROOM':
        flash('존재하지 않는 방입니다.')
    elif room_error == 'UNAUTHORIZED':
        flash('접근 권한이 없습니다.')

    if room_error:
        return redirect(url_for('main.home'))

    post_error = validate_post_access(room_id, post_id)

    if post_error == 'NOT_EXIST_POST':
        flash('게시글이 존재하지 않습니다.')
    elif post_error == 'INVALID_POST':
        flash('잘못된 접근입니다.')

    if post_error:
        return redirect(url_for('post.post_list', room_id=room_id))

    post = get_post_by_id(post_id)

    if post['author_id'] != ObjectId(user_id):
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    success = delete_post(post_id)

    if not success:
        flash('게시글 삭제에 실패했습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    flash('게시글이 삭제되었습니다.')
    return redirect(url_for('post.post_list', room_id=room_id))

# 댓글 작성
@post_bp.route('/rooms/<room_id>/posts/<post_id>/comments/write', methods=['POST'])
@login_required
def write_comment(room_id, post_id):
    user_id = session.get('user_id')
    user_name = session.get('username')

    post_error = validate_post_access(room_id, post_id)

    if post_error == 'NOT_EXIST_POST':
        flash('게시글이 존재하지 않습니다.')
    elif post_error == 'INVALID_POST':
        flash('잘못된 접근입니다.')

    if post_error:
        return redirect(url_for('post.post_list', room_id=room_id))

    content = request.form.get('content', '').strip()

    if not content:
        flash('댓글 내용을 입력하세요.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    create_comment(post_id, content, user_id, user_name)

    flash('댓글이 작성되었습니다.')
    return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

# 댓글 수정
@post_bp.route('/rooms/<room_id>/posts/<post_id>/comments/<comment_id>/edit', methods=['POST'])
@login_required
def edit_comment(room_id, post_id, comment_id):
    user_id = session.get('user_id')

    comment = get_comment_by_id(comment_id)

    if not comment:
        flash('댓글이 존재하지 않습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    if comment['author_id'] != ObjectId(user_id):
        flash('댓글 수정 권한이 없습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    content = request.form.get('content', '').strip()

    if not content:
        flash('댓글 내용을 입력하세요.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    success = update_comment(comment_id, content)

    if not success:
        flash('댓글 수정에 실패했습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    flash('댓글이 수정되었습니다.')
    return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

# 댓글 삭제
@post_bp.route('/rooms/<room_id>/posts/<post_id>/comments/<comment_id>/remove', methods=['POST'])
@login_required
def remove_comment(room_id, post_id, comment_id):
    user_id = session.get('user_id')

    comment = get_comment_by_id(comment_id)

    if not comment:
        flash('댓글이 존재하지 않습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    if comment['author_id'] != ObjectId(user_id):
        flash('댓글 삭제 권한이 없습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    success = delete_comment(comment_id)

    if not success:
        flash('댓글 삭제에 실패했습니다.')
        return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))

    flash('댓글이 삭제되었습니다.')
    return redirect(url_for('post.detail', room_id=room_id, post_id=post_id))