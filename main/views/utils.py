from flask import render_template, request, url_for, redirect, flash, session, g
from main.models import User, Post
from main import db
from functools import wraps


def login_required(f):  # デコレーターを定義。fはデコレートされるメソッド
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:  # ログインしてなかったらログイン画面にリダイレクト
            return redirect(url_for('user.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_view
