# coding=utf-8
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "sqlite:///app.db"
app.secret_key = "nothing"  # 记得设置 secret_key 不然有些东西会失效