# coding=utf-8
from app import app
from views import views

# 保存课表文件
views.login_credit.CACHE_SYLLABUS = True

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)