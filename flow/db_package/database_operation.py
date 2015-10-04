# coding=utf-8
import json
import os, sys
sys.path.append(os.path.abspath('..'))
from server import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

DATABASE_DIR = 'sqlite:///{base}users.db'.format(base=os.path.dirname(__file__) + os.path.sep)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_DIR
db = SQLAlchemy(app)

# 常量定义
USERNAME_PASSWORD_MAX_LENGTH = 30
USERNAME = "username"
PASSWORD = "password"
START_TIME = "start"
END_TIME = "end_time"
MAX_SHARE_THIS_TIME = "max_share_this_time"
SHARED_THIS_TIME = "shared_this_time"
TOTAL_SHARED = "total_shared"
FETCHED_THIS_TIME = "fetched_this_time"
TOTAL_FETCHED = "total_fetched"
SHARE_RATE = "share_rate"
HAS_BEEN_SHARED = "has_been_shared"
CREDIT = "credit"
CUR_ACCOUNT = "cur_account"
VALID = "valid"
MAX_LEFT_FLOW = "max_left_flow"

class User(db.Model):
    # 表名
    __tablename__ = "stu_account"

    username = db.Column(db.String(USERNAME_PASSWORD_MAX_LENGTH), primary_key=True, unique=True)
    password = db.Column(db.String(USERNAME_PASSWORD_MAX_LENGTH))
    # 开始、停止分享的时间，用 秒数表示
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    # 这次分享最多分享的流量数
    max_share_this_time = db.Column(db.Integer)
    # 本次已经分享的流量数
    shared_this_time = db.Column(db.Integer)
    # 该账号已经总共分享过的流量
    total_shared = db.Column(db.Integer)
    # 本次获取的流量
    fetched_this_time = db.Column(db.Integer)
    # 该账号总共获取过的流量
    total_fetched = db.Column(db.Integer)
    # 分享率
    share_rate = db.Column(db.REAL)
    # 在这段期间，该账号是否已经被分享过了
    has_been_shared = db.Column(db.Integer)
    # 用户信用
    credit = db.Column(db.Integer)
    # 目前在使用的账号
    cur_account = db.Column(db.String(USERNAME_PASSWORD_MAX_LENGTH))
    # 用户有效性
    valid = db.Column(db.Integer)
    # 剩余流量的最大值
    max_left_flow = db.Column(db.Integer)

    # 构建新的分享用户
    def __init__(self, user, passwd, start, end, max_, max_left_flow, shared_this_time=0, total_shared=0,
                 fetched_this_time=0, total_fetched=0, share_rate=0, has_been_shared=0, credit=100):
        self.username = user
        self.password = passwd
        self.start_time = start
        self.end_time = end
        self.max_share_this_time = max_
        self.max_left_flow = max_left_flow
        self.shared_this_time = shared_this_time
        self.total_shared = total_shared
        self.fetched_this_time = fetched_this_time
        self.total_fetched = total_fetched
        self.share_rate = share_rate
        self.has_been_shared = has_been_shared
        self.credit = credit
        self.cur_account = ""
        self.valid = 1

    def to_dict(self, password=False):
        dict_data = {
            "user":{
                USERNAME: self.username,
                START_TIME: self.start_time,
                END_TIME: self.end_time,
                MAX_SHARE_THIS_TIME: self.max_share_this_time,
                SHARED_THIS_TIME: self.shared_this_time,
                TOTAL_SHARED: self.total_shared,
                FETCHED_THIS_TIME: self.total_fetched,
                TOTAL_FETCHED: self.total_fetched,
                SHARE_RATE: self.share_rate,
                HAS_BEEN_SHARED: self.has_been_shared,
                CREDIT: self.credit,
                CUR_ACCOUNT: self.cur_account,
                VALID: self.valid,
                MAX_LEFT_FLOW: self.max_left_flow
            }
        }
        if password:
            dict_data[PASSWORD] = self.password
        return dict_data

    def to_json(self):
        return json.dumps(self.to_dict())

    def __repr__(self):
        return ("<{tablename} %r>" % self.username).format(tablename=self.__tablename__)

def add_user(user):
    db.create_all()
    try:
        db.session.add(user)
        db.session.commit()
        return True, None
    except IntegrityError as err:
        print(err)
        db.session.rollback()
        return False, str(err)

def get_user_by_name(username):
    user = User.query.filter_by(username=username).first()
    return user

def get_all_users_order_by_left_flow():
    return User.query.order_by(User.max_left_flow)

def get_all_users():
    return User.query.all()

def print_all_users(users):
    for user in users:
        print(user)
