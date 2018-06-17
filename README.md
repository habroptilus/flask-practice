# flask-practice

## DB作成

terminalでpythonをインタラクティブモードで立ち上げて、以下を実行。

```bash:terminal
from main.models import init
init()
```
`main/config.py`に書いてあるDBとテーブルを作成してくれる。
SQliteを使っている。

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
    * __init.py__(app,dbの初期化)
    * models.py(モデル)
    * views.py(ルーティング、コントローラ)
    * config.py(各自で作成)
* manage.py(アプリ実行用スクリプト)
* requirements.txt(ライブラリ一覧)
