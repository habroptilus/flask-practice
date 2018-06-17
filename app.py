from flask import Flask, render_template, request, url_for
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', message="こんにちは")


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


if __name__ == "__main__":
    app.run(debug=True)
