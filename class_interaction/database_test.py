# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from app import app
from datetime import datetime
import os

DIR_PATH = os.path.dirname(__file__)
DATA_BASE_NAME = "data_base.db"
FILE_NAME = os.path.join(DIR_PATH, DATA_BASE_NAME).replace("\\", "/")
DATA_BASE_URI = "sqlite:///" + FILE_NAME

app.config['SQLALCHEMY_DATABASE_URI'] = DATA_BASE_URI
db = SQLAlchemy(app)

CLASS_ID_LENGTH = 40
CLASS_NUMBER_LENGTH = 10
CLASS_NAME_LENGTH = 40
CLASS_CREDIT_LENGTH = 10
CLASS_TEACHER_LENGTH = 40
CLASS_ROOM_LENGTH = 10
CLASS_SPAN_LENGTH = 10
CLASS_TIME_LENGTH = 60

USER_NAME_LENGTH = 20
HW_CONTENT_LENGTH = 200

DISCUSS_CONTENT_LENGTH = 140

class ClassModel(db.Model):

    __tablename__ = "class_table"

    id = db.Column(db.Integer, primary_key=True)

    # 八个基本的属性
    # 课程的唯一标识符
    class_id = db.Column(db.String(CLASS_ID_LENGTH))
    # 班号
    class_number = db.Column(db.String(CLASS_NUMBER_LENGTH))
    # 名称
    class_name = db.Column(db.String(CLASS_NAME_LENGTH))
    # 学分
    class_credit = db.Column(db.String(CLASS_CREDIT_LENGTH))
    # 教师
    class_teacher = db.Column(db.String(CLASS_TEACHER_LENGTH))
    # 课室
    class_room = db.Column(db.String(CLASS_ROOM_LENGTH))
    # 跨度
    class_span = db.Column(db.String(CLASS_SPAN_LENGTH))
    # 时间
    class_time = db.Column(db.String(CLASS_TIME_LENGTH))

    # 关系区域

    # 一个课程对应多个作业
    class_homework = db.relationship("HomeworkModel",
                                     backref=db.backref("lesson"))

    # 对应多个评论
    class_discussion = db.relationship("DiscussModel",
                                       backref=db.backref("lesson"))


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Lesson %r>" % self.name

class HomeworkModel(db.Model):

    __tablename__ = "homework_table"

    id = db.Column(db.Integer, primary_key=True)

    # 发布者
    hw_publisher = db.Column(db.String(USER_NAME_LENGTH))
    # 发布时间
    hw_publish_time = db.Column(db.DateTime)
    # 上交时间
    hw_hand_in_time = db.Column(db.DateTime)
    # 内容
    hw_content = db.Column(db.String(HW_CONTENT_LENGTH))
    # 图片(留作扩展)
    hw_picture = db.Column(db.BLOB)

    # 外键
    hw_class = db.Column(db.Integer, db.ForeignKey("class_table.id"))

    def __init__(self, publisher, pub_time, hand_in_time, content, lesson):
        self.hw_publisher = publisher
        self.hw_publish_time = pub_time
        self.hw_hand_in_time = hand_in_time
        self.hw_content = content
        self.lesson = lesson

    def __repr__(self):
        return "<Homework %s %r>" % (self.hw_publisher, self.lesson) + self.hw_content

class DiscussModel(db.Model):

    __tablename__ = "discuss_table"

    id = db.Column(db.Integer, primary_key=True)

    # 发布者
    discuss_publisher = db.Column(db.String(USER_NAME_LENGTH))
    # 内容
    discuss_content = db.Column(db.String(DISCUSS_CONTENT_LENGTH))
    # 时间
    discuss_time = db.Column(db.DateTime)
    # 图片
    discuss_picture = db.Column(db.BLOB)

    # 外键
    discuss_class = db.Column(db.Integer, db.ForeignKey("class_table.id"))

    def __init__(self, publisher, content, when, lesson):
        self.discuss_publisher = publisher
        self.discuss_content = content
        self.discuss_time =  when
        # 应该是这个时候建立了联系
        self.lesson = lesson    # backref

    def __repr__(self):
        return "<Discussion %r %r>" % (self.discuss_publisher, self.discuss_time) + "\t" + self.discuss_content


def test():
    db.create_all()
    lesson = ClassModel("程序设计基础")
    print(lesson)
    homework = HomeworkModel("晓拂", datetime.now(), datetime.now(), "随便做点什么咯~不用交", lesson)
    discussion = DiscussModel("俊皓", "随便吹吹水咯", datetime.now(), lesson)
    print(homework)
    print(discussion)
    print(lesson, "\'s homework is", lesson.class_homework)
    print("the discussion is about", discussion.lesson)


if __name__ == "__main__":
    test()
