# coding=utf-8
# 用于用户交互的api

from . import database_test
from app import app
from flask import jsonify
from flask_restful import Api, Resource, reqparse, abort
from . import load_version  # 读取版本信息
import hashlib

database_test.db.create_all()

api = Api(app)

AUTHORIZE_CODE = "smallfly" # 测试用途

def check_hash(hash_code, input_string):
    result =  str(hashlib.sha256(input_string.encode("utf-8")).hexdigest())
    if hash_code == result:
        return True
    else:
        return False

def ret_vals_helper(func, arg, ok_msg):
    ret_vals = func(arg)
    if ret_vals[0]:
        # database_test.show_all_lessons()
        return jsonify(status=ok_msg)
    else:
        return jsonify(ERROR=ret_vals[1])

def class_arg_parser_helper(parser, location=('json', 'values',)):
    parser.add_argument("number", required=True, location=location)
    parser.add_argument("start_year", type=int, required=True, location=location)
    parser.add_argument("end_year", type=int, required=True, location=location)
    parser.add_argument("semester", required=True, type=int, location=location)

def query_class_by_class_id(class_id):
    lesson = database_test.ClassModel.query.filter_by(class_id=class_id).first()
    return lesson

class Cource(Resource):
    """
    用于添加课程
    """

    get_parser = reqparse.RequestParser()
    post_parser = reqparse.RequestParser()
    delete_parser = reqparse.RequestParser()

    def get(self):
        # 可以加可选的 location 参数 location=("args", )

        class_arg_parser_helper(self.get_parser, location= ("args", ))
        args = self.get_parser.parse_args()
        class_id = str(args['start_year']) + "_" + str(args["end_year"]) + "_" + str(args['semester']) + "_" + str(args['number'])
        lesson = database_test.ClassModel.query.filter_by(class_id=class_id).first()
        if lesson is not None:
            return jsonify(lesson=lesson.to_dict(), discussion=list(map(lambda x: x.to_dict(), lesson.class_discussion)),
                           homework=list(map(lambda x: x.to_dict(), lesson.class_homework)))
        else:
            return jsonify(ERROR="No such lesson")

    def post(self):
        # number, name, credit, teacher, room, span, time_, start_year, end_year, semester
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument("number", required=True)
        self.post_parser.add_argument("name", required=True)
        self.post_parser.add_argument("credit", required=True)
        self.post_parser.add_argument("teacher", required=True)
        self.post_parser.add_argument("room", required=True)
        self.post_parser.add_argument("span", required=True)
        self.post_parser.add_argument("time", required=True)
        self.post_parser.add_argument("start_year", required=True, type=int)
        self.post_parser.add_argument("end_year", required=True, type=int)
        self.post_parser.add_argument("semester", required=True, type=int)
        args = self.post_parser.parse_args()
        lesson = database_test.ClassModel(args["number"], args["name"], args['credit'], args['teacher'], args["room"],
        args["span"], args["time"], args["start_year"], args["end_year"], args["semester"])
        return ret_vals_helper(database_test.insert_to_database, lesson, "succeed to add the class")

    def delete(self):
        # 删除需要权限
        class_arg_parser_helper(self.delete_parser)
        args = self.delete_parser.parse_args()


        if args["authorize_code"] != AUTHORIZE_CODE:
            return jsonify(ERROR="Permission Denied")

        class_id = str(args['start_year']) + "_" + str(args["end_year"]) + "_" + str(args['semester']) + "_" + str(args['number'])


        lesson = database_test.ClassModel.query.filter_by(class_id=class_id).first()
        if lesson is not None:
            return ret_vals_helper(database_test.delete_from_database, lesson, "succeed to remove the class")
        else:
            return jsonify(ERROR="No such class")

api.add_resource(Cource, "/api/course", "/api/course/")

# 返回指定id课程的count条作业信息
def get_homework(id_, count):
    if count > 0:
        all_homework = database_test.HomeworkModel.query.filter(database_test.HomeworkModel.hw_class == id_).\
                    order_by(database_test.HomeworkModel.id.desc()).limit(count).all()
    else:   # 返回全部
        all_homework = database_test.HomeworkModel.query.filter(database_test.HomeworkModel.hw_class == id_).\
                    order_by(database_test.HomeworkModel.id.desc()).all()
    return all_homework

# 返回指定id课程的count条讨论信息
def get_discussion(id_, count):
    if count > 0:
        all_discussion = database_test.DiscussModel.query.filter(database_test.DiscussModel.discuss_class == id_).\
            order_by(database_test.DiscussModel.id.desc()).limit(count).all()
    else:
        all_discussion = database_test.DiscussModel.query.filter(database_test.DiscussModel.discuss_class == id_).\
            order_by(database_test.DiscussModel.id.desc()).all()
    return all_discussion

class CourseInformation(Resource):
    """
        用于获取课程信息
    """
    HOMEWORK = 0
    DISCUSSION = 1

    parser = reqparse.RequestParser()

    # 根据type_值返回不同数据
    def get(self, type_):
        # 对课程进行选择
        class_arg_parser_helper(self.parser, location=("args", ))
        # 在query字符中写上需要的数据量
        self.parser.add_argument("count", type=int, required=True, location=("args", ))
        args = self.parser.parse_args()
        class_id = str(args['start_year']) + "_" + str(args["end_year"]) + "_" + str(args['semester']) + "_" + str(args['number'])
        lesson = query_class_by_class_id(class_id)

        if lesson is None:
            return jsonify(ERROR="No such class")
        # 课程表的主键
        id_ = lesson.id

        if type_ == self.HOMEWORK:
            # 根据参数返回相应数据
            all_homework = get_homework(id_, args['count'])
            count = len(all_homework)
            if count == 0:
                return jsonify(ERROR="no homework")
            return jsonify(count=count, homework=list(map(lambda x: x.to_dict(), all_homework)))

        elif type_ == self.DISCUSSION:
            # 返回讨论信息
            all_discussions = get_discussion(id_, args['count'])
            count = len(all_discussions)
            if count == 0:
                return jsonify(ERROR="no discussion")
            return jsonify(count=count, discussions=list(map(lambda x: x.to_dict(), all_discussions)))
        else:
            abort(404)

api.add_resource(CourseInformation, "/api/course_info/<int:type_>")

class User(Resource):
    """
    用户
    """
    parser = reqparse.RequestParser()

    def get(self, name=""):
        if name == "":
            abort(404)
        user = database_test.UserModel.query.filter_by(user_account=name).first()
        if user is not None:
            return jsonify(user=repr(user))
        else:
            return jsonify(ERROR="no such user")

    def post(self):
        self.parser.add_argument("username", required=True)
        args = self.parser.parse_args()
        user = database_test.UserModel(args['username'])
        return ret_vals_helper(database_test.insert_to_database, user, user.user_certificate)

    # def delete(self, name=""):
    #     if name == "":
    #         abort(404)
    #     user = database_test.UserModel.query.filter_by(user_account=name).first()
    #     if user is None:
    #         return jsonify(ERROR="No such user")
    #     else:
    #         return ret_vals_helper(database_test.delete_from_database, user, "succeed to remove the user")

api.add_resource(User, "/api/user", "/api/user/<name>")


class Homework(Resource):
    """
    发布作业信息
    """
    # publisher, pub_time, hand_in_time, content, lesson

    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("publisher", required=True)
        self.parser.add_argument("pub_time", required=True, type=float)
        self.parser.add_argument("hand_in_time", required=True)
        self.parser.add_argument("content", required=True)
        self.parser.add_argument("code", required=True)  # hash_code

        class_arg_parser_helper(self.parser)
        args = self.parser.parse_args()

        user = database_test.UserModel.query.filter_by(user_account=args['publisher']).first()
        if user is None:
            return jsonify(ERROR="no such user")
        class_id = str(args['start_year']) + "_" + str(args["end_year"]) + "_" + str(args['semester']) + "_" + str(args['number'])
        lesson = database_test.ClassModel.query.filter_by(class_id=class_id).first()
        if lesson is None:
            return jsonify(ERROR="no such class")
        username = args['publisher']
        timestamp = str( int(args['pub_time']) )
        hash_code = args["code"]
        if not check_hash(hash_code, username+timestamp):
            return jsonify(ERROR="wrong code")
        from datetime import datetime
        # print(args['pub_time'])
        # print(datetime.now().timestamp())
        homework = database_test.HomeworkModel(user, datetime.fromtimestamp(float(args['pub_time'])),
                                               args['hand_in_time'], args['content'], lesson)
        return ret_vals_helper(database_test.insert_to_database, homework, "succeed to add the homework")


api.add_resource(Homework, "/api/homework")

class Discussion(Resource):
    """
    发布作业信息
    """
    # def __init__(self, publisher, content, when, lesson):

    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("publisher", required=True)
        self.parser.add_argument("pub_time", required=True, type=float)
        self.parser.add_argument("content", required=True)
        self.parser.add_argument("code", required=True)
        # 用于判断是对应哪一节课程
        class_arg_parser_helper(self.parser)
        args = self.parser.parse_args()
        user = database_test.UserModel.query.filter_by(user_account=args['publisher']).first()
        if user is None:
            return jsonify(ERROR="no such user")
        class_id = str(args['start_year']) + "_" + str(args["end_year"]) + "_" + str(args['semester']) + "_" + str(args['number'])
        lesson = database_test.ClassModel.query.filter_by(class_id=class_id).first()
        if lesson is None:
            return jsonify(ERROR="no such class")
        username = args['publisher']
        timestamp = str( int(args["pub_time"]) )
        hash_code = args["code"]
        if not check_hash(hash_code, username+timestamp):
            return jsonify(ERROR="wrong code")
        from datetime import datetime
        discussion = database_test.DiscussModel(user, args["content"], datetime.fromtimestamp(float(args['pub_time'])), lesson)
        return ret_vals_helper(database_test.insert_to_database, discussion, "succeed to add the discussion")


api.add_resource(Discussion, "/api/discuss")

class VersionControl(Resource):
    """
        用于控制app升级的api
    """
    VERSION_FILE = "version.txt"

    # 返回最新的版本号 versionCode 整型
    def get(self):
        version_obj = load_version.load_version()

        return jsonify(versionCode=version_obj['versionCode'], versionName=version_obj['versionName'],
                        versionDescription=version_obj['description'], versionDate=version_obj['versionDate'],
                       versionReleaser=version_obj['versionReleaser'], download_address=version_obj['download_address'],
                       apk_file_name=version_obj['apk_file_name'])

api.add_resource(VersionControl, "/api/version", "/api/version/")


if __name__ == "__main__":
    input_data = "e6f6a7a75c3a02b07bf3104be668ae5a9b02723b2fa6d00dedd908d7eaa04846"
    if check_hash(input_data, "smallfly2nd"):
        print("It's right")
    else:
        print("It's not right")