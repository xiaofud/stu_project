# coding=utf-8
from app import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from class_interaction import database_test

admin = Admin(app, name="syllabus_test", template_mode="bootstrap3")
admin.add_view(ModelView(database_test.ClassModel, database_test.db.session))
admin.add_view(ModelView(database_test.UserModel, database_test.db.session))
admin.add_view(ModelView(database_test.DiscussModel, database_test.db.session))
admin.add_view(ModelView(database_test.HomeworkModel, database_test.db.session))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)