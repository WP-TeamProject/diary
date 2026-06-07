from flask import redirect, url_for, flash, session
from functools import wraps

# 로그인 여부 확인
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = session.get('user_id')

        if not user_id:
            flash('로그인이 필요합니다.')
            return redirect(url_for('user.login'))

        return view(*args, **kwargs)

    return wrapped_view

# 관리자 권한 확인
def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_role = session.get('role')

        if user_role != 'admin':
            flash('관리자 권한이 필요합니다.')
            return redirect(url_for('main.home'))

        return view(*args, **kwargs)

    return wrapped_view