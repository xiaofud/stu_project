# coding=utf-8
from app import app
from flask import render_template, request, jsonify, url_for, redirect, make_response, send_from_directory
# from credit import login_credit
from credit import class_info_parser, authentication
from oa import oa_main
from class_interaction import database_test
from credit import syllabus_getter
from credit import error_string
from credit import grade_getter


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
        ret_val = syllabus_getter.get_syllabus(user, passwd, start_year=start_year, end_year=end_year, semester=semester, timeout=5)
        if ret_val[0]:
            content = ret_val[1]
            lessons = syllabus_getter.parse(content.decode("UTF-8"))
            if len(lessons) == 0:
                return jsonify(ERROR="No classes")
            else:
                # 课程的json数据
                lessons_jsonfy = class_info_parser.Lesson.jsonfy_all(lessons)
                # 这里插入用户
                account = database_test.UserModel.query.filter_by(user_account=user).first()
                if account is None:
                    account = database_test.UserModel(user)
                    # 加入数据库
                    ret_vals = database_test.insert_to_database(account)
                    if ret_vals[0]: # 插入成功
                        # "token":"279456"
                        token_json = "\"token\":" + "\"{}\"".format(account.user_certificate)
                        lessons_jsonfy = lessons_jsonfy[: -1] + "," + token_json + "}"
                # the user exists
                else:
                    # 生成新的token
                    new_token = database_test.generate_certificate(database_test.CERTIFICATE_LENGTH)
                    account.user_certificate = new_token
                    # 提交更改
                    database_test.db.session.commit()
                    token_json = "\"token\":" + "\"{}\"".format(account.user_certificate)
                    lessons_jsonfy = lessons_jsonfy[: -1] + "," + token_json + "}"
            # return render_template("show_classes.html", lessons=lessons)
                if syllabus_getter.CACHE_SYLLABUS:
                    filename = user + "_" + "{}_{}".format(start_year, end_year) + "_" + str(semester)
                    syllabus_getter.save_file(filename, lessons_jsonfy)
                return lessons_jsonfy
        else:
            return jsonify(ERROR=error_string.err_srt(ret_val[1]))
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
        return jsonify(GRADES=grade_getter.parse_grades(ret_val[1]))

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