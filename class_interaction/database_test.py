# coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
DATA_BASE_URI = "sqlite:///test.db"

test_app = Flask(__name__)
test_app.config['SQLALCHEMY_DATABASE_URI'] = DATA_BASE_URI
db = SQLAlchemy(test_app)

class Lesson(db.Model):

    __tablename__ = "lesson"

    id = db.Column(db.Integer, primary_key=True)
    name = db.String(db.String(30))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Lesson %r>" % self.name

class Comment(db.Model):

    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    # 评论
    content = db.Column(db.String(140))
    # 发布者
    commenter = db.Column(db.String(20))

    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))
    # relationship 'lesson' expects a class or a mapper argument
    lesson = db.relationship(Lesson, backref=db.backref('comments'))

    def __init__(self, commenter, content, lesson):
        self.commenter = commenter
        self.content = content
        # 应该是这个时候建立了联系
        self.lesson = lesson

    def __repr__(self):
        return "<comment %r>" % self.commenter + "\t" + self.content


def test():
    db.create_all()
    lesson = Lesson("Math")
    print(lesson)
    comment = Comment("smallfly", "It's important", lesson)
    comment2 = Comment("smallfly", "This's a test", None)
    # 到这里神奇的又把 comment2 的lesson赋值为了Math class
    lesson.comments.append(comment2)
    print(lesson.comments)

    print(comment.lesson)
    print(comment2.lesson)

if __name__ == "__main__":
    test()

# from datetime import datetime
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80))
#     body = db.Column(db.Text)
#     pub_date = db.Column(db.DateTime)
#
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
#     category = db.relationship('Category',
#         backref=db.backref('posts', lazy='dynamic'))
#
#     def __init__(self, title, body, category, pub_date=None):
#         self.title = title
#         self.body = body
#         if pub_date is None:
#             pub_date = datetime.utcnow()
#         self.pub_date = pub_date
#         self.category = category
#
#     def __repr__(self):
#         return '<Post %r>' % self.title
#
# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return '<Category %r>' % self.name