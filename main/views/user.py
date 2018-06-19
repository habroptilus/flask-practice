from flask import Blueprint
from flask import render_template, request, url_for, redirect, flash, session, g
from main.models import User, Post
from main import db
from functools import wraps
from main.views.utils import login_required

app = Blueprint("user", __name__, template_folder="templates")


@app.route("/index")
@login_required
def index():
    user_list = User.query.all()
    message = "Hello {}!".format(g.user.username)
    return render_template('index.html', message=message, user_list=user_list)


@app.route("/add_user", methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if username:
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('user.index'))


@app.route("/user/<user_id>")
@login_required
def show_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    posts = db.session.query(Post).filter_by(user_id=user_id)
    return render_template("show_user.html", target_user=target_user, posts=posts)


@app.route("/user/delete/<user_id>", methods=['POST'])
def del_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    db.session.delete(target_user)
    db.session.commit()
    return redirect(url_for("user.index"))


@app.route("/user/edit/<user_id>", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    if request.method == 'GET':
        return render_template("edit_user.html", target_user=target_user)
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        target_user.username = username
        target_user.email = email
        target_user.password = password
        db.session.commit()
        return redirect(url_for("user.index"))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, authenticated = User.authenticate(db.session.query,
                                                request.form['email'], request.form['password'])
        if authenticated:
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(url_for('user.index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('user.login'))
