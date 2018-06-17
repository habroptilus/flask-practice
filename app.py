from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username


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


if __name__ == "__main__":
    app.run(debug=True)
