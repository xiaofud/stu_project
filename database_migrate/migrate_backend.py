# coding = utf-8

"""
    管理数据库迁移
"""

from class_interaction.database_models import db
from app import app
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)