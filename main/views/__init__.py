from flask import Flask, session, g
from main.views import user, post, practice
from main.models import User
from main import application


@application.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


modules_define = [user.app, post.app, practice.app]
for app in modules_define:
    application.register_blueprint(app)
