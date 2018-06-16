from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', message="こんにちは")


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # postできた場合。テキストエリア"hoge"の値を埋め込んでレンダリング
        val = request.form['hoge']
    else:
        # getできた場合。クエリパラメータをこれで受け取れる。なかったら第二引数のを用いる
        val = request.args.get("msg", "Not defined")
    return render_template('test.html', result=val)


if __name__ == "__main__":
    app.run(debug=True)
