# coding=utf-8
from app import app
from migrate_manager import User, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name="migrate_test", template_mode="bootstrap3")

admin.add_view(ModelView(User, db.session))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)