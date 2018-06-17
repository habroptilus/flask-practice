from flask import render_template, request, url_for, redirect
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


@app.route('/hoge/<postid>')
def hoge(postid):
    return render_template('hoge.html', result='id = {}'.format(postid))


@app.route("/add_user", methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username:
        user = User(username)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('index'))


@app.route("/user/<user_id>")
def show_user(user_id):
    target_user = User.query.get(user_id)  # primary keyでなら検索できる

    return render_template("show_user.html", target_user=target_user)
