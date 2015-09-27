from flask import Flask, render_template, request, jsonify
from  credit import login_credit
from credit import get_course_info
from oa import oa_main

# import sys
# print(sys.path)

app = Flask(__name__)
app.config['SECRET_KEY'] = "Nothing secret yet"

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
        ret_val = login_credit.connect(user, passwd, start_year=start_year, end_year=end_year, semester=semester)
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
    return render_template("login.html")

@app.route('/oa')
def get_updated_information():
    information = oa_main.get_most_updated()    # list of dict
    return jsonify(notifications=information)
    # return information

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')