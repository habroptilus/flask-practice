from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('main.config')  # config.pyを読み込んで設定
db = SQLAlchemy(app)    # dbをオブジェクトにする

import main.views
