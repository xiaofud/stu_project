# coding=utf-8
from app import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from class_interaction import database_models

admin = Admin(app, name="syllabus_test", template_mode="bootstrap3")
admin.add_view(ModelView(database_models.ClassModel, database_models.db.session))
admin.add_view(ModelView(database_models.UserModel, database_models.db.session))
admin.add_view(ModelView(database_models.DiscussModel, database_models.db.session))
admin.add_view(ModelView(database_models.HomeworkModel, database_models.db.session))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)