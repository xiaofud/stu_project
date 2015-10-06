# coding=utf-8
from app import app
from flask import render_template, request, jsonify, url_for, redirect
from  credit import login_credit
from credit import get_course_info, authentication
from oa import oa_main

@app.errorhandler(404)
def page_not_found(err):
    print(err)
    return redirect(url_for('index'))

@app.route('/')
def index():
    urls = dict()
    urls['syllabus'] = url_for('query', _external=True)
    urls['oa'] = url_for('get_updated_information', _external=True)
    urls['auth'] = url_for('stu_auth', _external=True)
    return render_template('home.html', urls=urls)

# 课程表
@app.route('/syllabus', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        user = request.form['username']
        passwd = request.form['password']
        years = request.form['years']
        start_year, end_year = years.split("-")
        start_year = int(start_year)
        end_year = int(end_year)
        semester = int(request.form['semester'])
        print(user, start_year, end_year, semester)
        ret_val = login_credit.connect(user, passwd, start_year=start_year, end_year=end_year, semester=semester, timeout=5)
        if ret_val[0]:
            raw = ret_val[1]
            lessons = login_credit.parse(raw.decode('gbk'))
            if len(lessons) == 0:
                return jsonify(ERROR="No classes")
            else:
                lessons = get_course_info.Lesson.jsonfy_all(lessons)
            # return render_template("show_classes.html", lessons=lessons)
                return lessons
        else:
            return jsonify(ERROR=login_credit.err_srt(ret_val[1]))
    return render_template('login.html')

# 办公自动化
@app.route('/oa')
def get_updated_information():
    information = oa_main.get_most_updated()    # list of dict
    return jsonify(notifications=information)
    # return information

# 验证用户
@app.route("/auth", methods=["GET", "POST"])
def stu_auth():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username.strip() == "" or password.strip() == "":
            return jsonify(Error="invalid input")
        else:
            ret_val = authentication.authenticate_by_credit(username, password)
            if ret_val == authentication.CORRECT:
                return jsonify(status="correct")
            elif ret_val == authentication.INCORRECT:
                return jsonify(status="incorrect")
            elif ret_val == authentication.TIMEDOUT:
                return jsonify(status="timeout")
    else:
        return render_template("auth.html")