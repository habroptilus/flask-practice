from flask import Blueprint
from flask import render_template, request, url_for, redirect, session, g
from main.models import User, Post
from main import db
from functools import wraps
from main.views.utils import login_required


app = Blueprint("post", __name__)


@app.route("/create_post/<user_id>", methods=['GET', 'POST'])
@login_required
def add_post(user_id):
    if request.method == 'POST':
        body = request.form.get('body')
        title = request.form.get('title')

        if body and title:
            post = Post(user_id, title, body)
            db.session.add(post)
            db.session.commit()
            return redirect("/user/{}".format(user_id))
    target_user = User.query.get(user_id)
    return render_template("create_post.html", target_user=target_user)


@app.route("/show_post/<post_id>")
@login_required
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template("show_post.html", post=post)


@app.route("/edit_post/<post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    target_post = Post.query.get(post_id)  # primary keyでなら検索できる
    if request.method == 'GET':
        return render_template("edit_post.html", target_post=target_post)
    elif request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        target_post.title = title
        target_post.body = body
        db.session.commit()
        return redirect(url_for("post.show_post", post_id=target_post.id))


@app.route("/delete_post/<post_id>", methods=['POST'])
def del_post(post_id):
    target_post = Post.query.get(post_id)  # primary keyでなら検索できる
    user_id = User.query.get(target_post.user_id).id
    db.session.delete(target_post)
    db.session.commit()
    return redirect(url_for("user.show_user", user_id=user_id))
