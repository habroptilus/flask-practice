from flask import render_template, request, url_for, redirect, flash, session
from main.models import User
from main import db, app


@app.route("/")
def index():
    user_list = User.query.all()
    return render_template('index.html', message="こんにちは", user_list=user_list)


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
def show_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    return render_template("show_user.html", target_user=target_user)


@app.route("/user/delete/<user_id>", methods=['POST'])
def del_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる
    db.session.delete(target_user)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/user/edit/<user_id>", methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
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
