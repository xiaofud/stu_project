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
CERTIFICATE_LENGTH = 6     # 6个数字组成的认证码

USER_NAME_LENGTH = 20
HW_CONTENT_LENGTH = 200

DISCUSS_CONTENT_LENGTH = 140

SEMESTERS = {
    "spring": 2,
    "summber": 3,
    "autumn": 1
}

def generate_certificate(length):
    import random
    random_str = ""
    for i in range(length):
        num = random.randint(0, 9)
        random_str += str(num)
    return random_str


# 关联表
user_class_association_table = db.Table("user_class_association_table", db.Model.metadata,
    db.Column("class_id", db.Integer, db.ForeignKey("class_table.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user_table.id"))
)


class UserModel(db.Model):
    """
        这张表和 课表 是多对多的关系, 与课表的关系是双向的, 在这张表里面引用课表是用 lessons
    """
    __tablename__ = "user_table"

    # 基本字段
    id = db.Column(db.Integer, primary_key=True)

    # 用户账号
    user_account = db.Column(db.String(USER_NAME_LENGTH), unique=True)

    # 凭证 10 个随机数字组成的认证码
    user_certificate = db.Column(db.String(CERTIFICATE_LENGTH))

    # 用户有效性 取值 0 1, 用于封禁用户
    user_validity = db.Column(db.Integer)

    # 用户评论
    user_discussion = db.relationship("DiscussModel", backref="user")

    # 用户发布的作业
    user_homework = db.relationship("HomeworkModel", backref="user")

    def __init__(self, account):
        self.user_account = account
        self.user_validity = 1
        self.user_certificate = generate_certificate(CERTIFICATE_LENGTH)

    def __repr__(self):
        return "<User %r>" % self.user_account + self.user_certificate


class ClassModel(db.Model):

    __tablename__ = "class_table"

    # id 的值是从1开始的
    id = db.Column(db.Integer, primary_key=True)

    # 八个基本的属性
    # 课程的唯一标识符 格式 年份_学期_班号 比如 2015_2016_[123]_66666
    # 学期用 数字代表
    class_id = db.Column(db.String(CLASS_ID_LENGTH), unique=True)
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

    # 课程与学生是多对多的关系
    class_members = db.relationship("UserModel", secondary=user_class_association_table,
                                    backref="lessons")


    def __init__(self, number, name, credit, teacher, room, span, time_, start_year, end_year, semester):
        self.class_number = number
        self.class_name = name
        self.class_credit = credit
        self.class_teacher = teacher
        self.class_room = room
        self.class_span = span
        self.time = time_
        # 每一节课程的唯一标识
        self.class_id = str(start_year) + "_" + str(end_year) + "_" + str(semester) + "_" + self.class_number



    def __repr__(self):
        return "<Lesson %r>" % self.class_name + str(self.class_homework) + str(self.class_discussion)

class HomeworkModel(db.Model):

    __tablename__ = "homework_table"

    id = db.Column(db.Integer, primary_key=True)

    # 发布者 修改为外键了
    # hw_publisher = db.Column(db.String(USER_NAME_LENGTH))

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
    hw_publisher = db.Column(db.Integer, db.ForeignKey("user_table.id"))

    def __init__(self, publisher, pub_time, hand_in_time, content, lesson):
        self.user = publisher
        self.user.lessons.append(lesson)

        self.hw_publish_time = pub_time
        self.hw_hand_in_time = hand_in_time
        self.hw_content = content
        self.lesson = lesson


    def __repr__(self):
        return "<Homework %r>" % self.user + self.hw_content

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
    discuss_user = db.Column(db.Integer, db.ForeignKey("user_table.id"))

    def __init__(self, publisher, content, when, lesson):
        self.user = publisher
        self.user.lessons.append(lesson)
        self.discuss_content = content
        self.discuss_time =  when
        # 应该是这个时候建立了联系
        self.lesson = lesson    # backref

    def __repr__(self):
        return "<Discussion %r %r>" % (self.user, self.discuss_time) + "\t" + self.discuss_content


def insert_to_database(thing):
    try:
        db.session.add(thing)
        db.session.commit()
        return True, None
    except Exception as e:
        # don't forget to do this
        db.session.rollback()
        print(type(e))
        return False, str(e)

def delete_from_database(thing):
    try:
        db.session.delete(thing)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        print(type(e))
        return False, str(e)



def test():
    db.drop_all()
    db.create_all()
    nwad = UserModel("拂晓")
    junhao = UserModel("俊皓")
    lesson = ClassModel("4040", "程序设计基础", "4.0", "方若宇", "E301", "1-16", datetime.now(), 2015, 2016, SEMESTERS['spring'])

    discuss_nwad = DiscussModel(nwad, "How Are you ?", datetime.now(), lesson)
    discuss_junhao = DiscussModel(junhao, "I'm fine.Thanks", datetime.now().replace(minute=15), lesson)

    homework = HomeworkModel(nwad, datetime.now(), datetime.now().replace(day=12), "图形学", lesson)

    ret_vats = insert_to_database(lesson)
    if not ret_vats[0]:
        print(ret_vats[1])
    # print(HomeworkModel.query.all())
    # print(DiscussModel.query.all())
    # print(UserModel.query.all())
    print(get_last_inserted_record(HomeworkModel))
    print(get_last_inserted_record(DiscussModel))
    print(get_last_inserted_record(ClassModel))


def get_last_inserted_record(model):
    the_latest = model.query.order_by(model.id.desc()).first()
    return the_latest

# db.create_all()

if __name__ == "__main__":
    test()
    # now = datetime.now()
    # print(now)
    # import time
    # now = datetime.fromtimestamp(time.time())
    # print(now)


# for debug
# xiaofu = UserModel("晓拂")
    # junhao = UserModel("俊皓")
    # lesson = ClassModel("66666", "程序设计基础", "4.0", "方若宇", "E201", "1-16", "None,67,None,None,67,None,None", 2014, 2015, SEMESTERS['autumn'])
    # homework = HomeworkModel(xiaofu, datetime.now(), datetime.now(), "随便做点什么咯~不用交", lesson)
    # discussion = DiscussModel(junhao, "How are you?", datetime.now(), lesson)
    # discussion = DiscussModel(xiaofu, "I'm fine.Thanks", datetime.now(), lesson)
    # lesson2 = ClassModel("44444", "高等数学", "4.0", "方若宇", "E201", "1-16", "None,67,None,None,67,None,None", 2014, 2015, SEMESTERS['autumn'])
    # # 与之相关联的 评论和作业也会加入到数据库中
    # ret_vals = insert_class(lesson)
    # print(lesson.id)
    # insert_class(lesson2)
    # if not ret_vals[0]:
    #     print(ret_vals[1])
    #
    # get_last_inserted_record()
    #
    # # filter_by 返回的对象类型是 <class 'flask_sqlalchemy.BaseQuery'>
    # # .first() 当没有数据的时候 返回的是 None
    # programming = ClassModel.query.filter_by(class_name="程序设计基").first()
    # # print(type(programming))
    # if programming is None:
    #                                           # 这里 Column 对象有 自己的 contains 方法，而不是str的 __contains__ 方法
    #     programming = ClassModel.query.filter(ClassModel.class_name.contains("程序设计基")).first()
    # if programming is not None:
    #     print(programming)
    #     print(programming.class_homework)
    #     print(programming.class_discussion)
    # else:
    #     print("No such data")
    #
    # # 删除数据
    # db.session.delete(programming)
    # # 删除数据也要记得commit(), 总之做出改变的都要
    # db.session.commit()
    # # 删除数据并不会删除其关系里面的其他记录
    # programming = ClassModel.query.filter_by(class_name="程序设计基础").first()
    # if programming is None:
    #     print("deleted!")
    #     homework = HomeworkModel.query.all()
    #     for work in homework:
    #         print(work)
    #         print(work.id)