# coding=utf-8

from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from migrate_test import *



db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    # SQLITE3 原生不支持修改、删除COLUMN
    habit = db.Column(db.String(128))
    saying = db.Column(db.String(34))

if __name__ == "__main__":
    manager.run()