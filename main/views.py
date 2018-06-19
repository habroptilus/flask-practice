from flask import render_template, request, url_for, redirect, flash, session, g
from main.models import User, Post
from main import db, app
from functools import wraps


def login_required(f):  # デコレーターを定義。fはデコレートされるメソッド
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:  # ログインしてなかったらログイン画面にリダイレクト
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_view


@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


@app.route("/index")
@login_required
def index():
    user_list = User.query.all()
    message = "Hello {}!".format(g.user.username)
    return render_template('index.html', message=message, user_list=user_list)


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # postできた場合。テキストエリア"hoge"の値を埋め込んでレンダリング
        val = request.form.get('hoge')
        checked = request.form.getlist("list")
    else:
        # getできた場合。クエリパラメータをこれで受け取れる。なかったら第二引数のを用いる
        val = request.args.get("msg", "Not defined")
        checked = []
    return render_template('test.html', result=val, checked_list=checked)


@app.route("/add_user", methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if username:
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('index'))


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
    return redirect(url_for("index"))


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
        return redirect(url_for("index"))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, authenticated = User.authenticate(db.session.query,
                                                request.form['email'], request.form['password'])
        if authenticated:
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('login'))

# Posts


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
        return redirect(url_for("show_post", post_id=target_post.id))


@app.route("/delete_post/<post_id>", methods=['POST'])
def del_post(post_id):
    target_post = Post.query.get(post_id)  # primary keyでなら検索できる
    user_id = User.query.get(target_post.user_id).id
    db.session.delete(target_post)
    db.session.commit()
    return redirect(url_for("show_user", user_id=user_id))
