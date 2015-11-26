# coding=utf-8
from app import app
from flask import render_template, request, jsonify, url_for, redirect, make_response, send_from_directory
# from credit import login_credit
from credit import class_info_parser, authentication
from oa import oa_main
from class_interaction import database_models
from credit import syllabus_getter
from credit import error_string
from credit import grade_getter, exam_getter


@app.errorhandler(404)
def page_not_found(err):
    print(err)
    return redirect(url_for('index'))

# 默认页面
@app.route('/')
def index():
    urls = dict()
    urls['syllabus'] = url_for('query', _external=True)
    urls['oa'] = url_for('get_updated_information', _external=True)
    urls['auth'] = url_for('stu_auth', _external=True)
    urls['grade'] = url_for('query_grades', _external=True)
    urls['exam'] = url_for('query_exam', _external=True)
    return render_template('home.html', urls=urls)

@app.route("/exam", methods=['GET', 'POST'])
def query_exam():
    # 查看考试
    if request.method == "GET":
        return render_template("exam_info.html")
    user = request.form['username']
    password = request.form['password']
    years = request.form['years']
    start_year, end_year = years.split("-")
    start_year = int(start_year)
    end_year = int(end_year)
    semester = int(request.form['semester'])

    ret_val = exam_getter.get_exam_list(user, password, start_year, end_year, semester, timeout=7)
    if not ret_val[0]:
        return jsonify(ERROR=error_string.err_srt(ret_val[1]))
    else:
        return jsonify(EXAMS=ret_val[1])



# 课程表
@app.route('/syllabus', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        years = request.form['years']
        start_year, end_year = years.split("-")
        start_year = int(start_year)
        end_year = int(end_year)
        semester = int(request.form['semester'])
        print(user, start_year, end_year, semester)
        ret_val = syllabus_getter.get_syllabus(user, password, start_year=start_year, end_year=end_year, semester=semester, timeout=7)
        if ret_val[0]:
            content = ret_val[1]
            lessons = syllabus_getter.parse(content.decode("UTF-8"))
            if len(lessons) == 0:
                return jsonify(ERROR="No classes")
            else:
                # 课程的json数据
                lessons_json_data = class_info_parser.Lesson.jsonfy_all(lessons)
                # 这里查找用户
                account = database_models.UserModel.query.filter_by(user_account=user).first()
                # 进行这次课表查询的用户还不在数据库中
                if account is None:
                    print(user + " 是新用户")
                    account = database_models.UserModel(user)
                    # 默认昵称为帐号名
                    account.user_nickname = user
                    # 查看是否之前有人已经修改名字为这个账号名称
                    fake_user = database_models.query_user_by_nickname(user)
                    if fake_user is not None:
                        # 将用户名改回去
                        print("fake user is " + str(fake_user))
                        fake_user.user_nickname = fake_user.user_account
                        # 提交修改
                        database_models.commit()
                    # 加入数据库
                    ret_vals = database_models.insert_to_database(account)
                    if ret_vals[0]: # 插入成功
                        # "token":"279456"
                        token_json = "\"token\":" + "\"{}\"".format(account.user_certificate)
                        nickname_json = "\"nickname\":" + "\"{}\"".format(account.user_nickname)
                        lessons_json_data = lessons_json_data[: -1] + "," + token_json + "}"
                        lessons_json_data = lessons_json_data[: -1] + "," + nickname_json + "}"
                # the user exists
                else:
                    # 生成新的token
                    new_token = database_models.generate_certificate(database_models.CERTIFICATE_LENGTH)
                    account.user_certificate = new_token
                    # 提交更改
                    database_models.db.session.commit()
                    token_json = "\"token\":" + "\"{}\"".format(account.user_certificate)
                    lessons_json_data = lessons_json_data[: -1] + "," + token_json + "}"
                    # 添加nickname的返回
                    nickname_json = "\"nickname\":" + "\"{}\"".format(account.user_nickname)
                    lessons_json_data = lessons_json_data[: -1] + "," + nickname_json + "}"
                    # print(account.user_nickname)
            # return render_template("show_classes.html", lessons=lessons)
                if syllabus_getter.CACHE_SYLLABUS:
                    filename = user + "_" + "{}_{}".format(start_year, end_year) + "_" + str(semester)
                    syllabus_getter.save_file(filename, lessons_json_data)
                return lessons_json_data
        else:
            return jsonify(ERROR=error_string.err_srt(ret_val[1]))
    return render_template('login.html')

# 办公自动化
@app.route('/oa', methods=["GET", "POST"])
def get_updated_information():

    # modified by junhaow
    if request.method == "POST":

        username = request.form['username']
        token = request.form['token']

        if username.strip() == "" or token.strip() == "":
            return jsonify(ERROR="invalid input")
        elif not check_token(username, token):
            return jsonify(ERROR="wrong token")
        else:
            pageindex = request.form['pageindex']
            # 这个参数不需要
            # pagesize = request.form['pagesize']

            information = oa_main.get_most_updated(pageindex)
            return jsonify(DOCUMENTS=information)
    else:
        # 返回最新的 oa
        return oa_main.get_most_updated(1)

# token
def check_token(username, token):
    user = database_models.UserModel.query.filter_by(user_account=username).first()
    if user is not None:
        print(user.user_account, user.user_certificate)
        if user.user_certificate == token:
            return True
    return False


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

@app.route("/grade", methods=["GET", "POST"])
def query_grades():
    if request.method == "GET":
        return render_template("grade.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        ret_val = grade_getter.get_grades_raw_data(username, password, 7)
        if not ret_val[0]:
            return jsonify(ERROR=error_string.err_srt(ret_val[1]))
        grade_list, gpa = grade_getter.parse_grades(ret_val[1])
        if len(grade_list) == 0:
            return jsonify(ERROR="there is no information about grade")
        return jsonify(GRADES=grade_list, GPA=gpa)

@app.route("/qr")
def get_qr_code():
    return render_template("QR_page.html", src="QR.png")


import os
FILENAME = os.path.join(os.path.dirname(__file__), "news")

@app.route("/news")
def get_message():
    # news = None
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            news = f.read()
        return jsonify(news=news)
    else:
        return jsonify(Error="no news")


# def transform(text_file_contents):
#     return text_file_contents.replace("=", ",")


# @app.route('/transfer')
# def form():
#     return """
#         <html>
#             <body>
#                 <h1>Transform a file demo</h1>
#
#                 <form action="/transform" method="post" enctype="multipart/form-data">
#                     <input type="file" name="data_file" />
#                     <input type="submit" />
#                 </form>
#             </body>
#         </html>
#     """
#
# @app.route('/transform', methods=["POST"])
# def transform_view():
#     file = request.files['data_file']
#     if not file:
#         return "No file"
#
#     file_contents = file.stream.read().decode("utf-8")
#
#     result = transform(file_contents)
#
#     response = make_response(result)
#     response.headers["Content-Disposition"] = "attachment; filename=result.csv"
#     return response

# @app.route('/download/<string:filename>')
# def download(filename):
#     return send_from_directory(directory=app.root_path, filename=filename, as_attachment=True)