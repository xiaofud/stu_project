# coding=utf-8

from flask_sqlalchemy import SQLAlchemy
from app import app
import os

DIR_PATH = os.path.dirname(__file__)
DATA_BASE_NAME = "data_base.db"
FILE_NAME = os.path.join(DIR_PATH, DATA_BASE_NAME).replace("\\", "/")
DATA_BASE_URI = "sqlite:///" + FILE_NAME

app.config['SQLALCHEMY_DATABASE_URI'] = DATA_BASE_URI
db = SQLAlchemy(app)

association_table = db.Table('association', db.Model.metadata,
    db.Column('left_id', db.Integer, db.ForeignKey('left.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('right.id'))
)

class Parent(db.Model):
    __tablename__ = 'left'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    children = db.relationship("Child",
                    secondary=association_table,
                    backref="parents")
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Parent of %r>" % self.children

class Child(db.Model):
    __tablename__ = 'right'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Child %r>" % self.name


def test():
    p = Parent("Fantasy")
    c = Child(name="nwad")
    p.children.append(c)
    print(c.parents)
    print(p.children)

if __name__ == "__main__":
    test()