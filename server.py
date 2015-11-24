# coding=utf-8
from app import app
from views import views
# web api
import class_interaction.interaction_api_v1
class_interaction.interaction_api_v1.api.init_app(app)
# admin
# from stu_admin import syllabus_admin
# import stu_admin.syllabus_admin

# 保存课表文件
views.syllabus_getter.CACHE_SYLLABUS = True

# 创建特殊课程时需要
# from class_interaction.add_public_lesson import add_public_class

# add_public_class()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)