# flask-practice

## DB作成

terminalでpythonをインタラクティブモードで立ち上げて、以下を実行。

```bash:terminal
from main.models import init_db
init_db()
```
`main/config.py`に書いてあるDBとテーブルを作成してくれる。
SQliteを使っている。

登録されたユーザーがいないとログインできなくなってしまうので、DBを作成すると同時に管理者ユーザーを作成するようにしている。
管理者ユーザー情報は以下。

```
username : administrator
email : admin@example.com
password : admin
```

## ライブラリ

requirements.txtに必要なライブラリ一覧が記載されている。
pipでインストールする場合には以下を実行。

```bash:terminal
pip install -r requirements.txt
```

## ディレクトリ構成

* main
    * static(css,JS)
    * templates(html)
    * __init.py__(application,dbの初期化)
    * models.py(モデル)
    * views.py(ルーティング、コントローラ)
    * config.py(各自で作成)
* manage.py(アプリ実行用スクリプト)
* requirements.txt(ライブラリ一覧)

内部の仕組みは次の通り。

1. main.__init__.pyでapplicationとdbの初期化
1. このapplicationをviews.__init__.pyで読んでルーティング
1. ルーティングしたapplicationをmanage.pyで実行
