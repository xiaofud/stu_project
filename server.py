# coding=utf-8
from app import app
from views import views
import class_interaction.interaction_api

# 保存课表文件
views.login_credit.CACHE_SYLLABUS = True

if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.100', port=5000)