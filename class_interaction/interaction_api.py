# coding=utf-8
# 用于用户交互的api

import database_test
from app import app
from flask_restful import Api, Resource, output_json, reqparse, abort

database_test.db.create_all()

api = Api(app)

def ret_vals_helper(func, arg, ok_msg, ok_code=200, err_code=0):
    ret_vals = func(arg)
    if ret_vals[0]:
        return output_json(dict(status=ok_msg), ok_code)
    else:
        return output_json(dict(ERROR=ret_vals[1]), err_code)

class Cource(Resource):
    """
    用于添加课程
    """

    parser = reqparse.RequestParser()

    def get(self, name=""):
        if name == "":
            return output_json(dict(ERROR="you should provide class name information"), 0)
        lesson = database_test.ClassModel.query.filter_by(class_name=name).first()
        if lesson is not None:
            return output_json(dict(lesson=repr(lesson)), 200)
        else:
            return output_json(dict(ERROR="No such lesson"), 0)

    def post(self):
        # number, name, credit, teacher, room, span, time_, start_year, end_year, semester
        self.parser.add_argument("number", required=True)
        self.parser.add_argument("name", required=True)
        args = self.parser.parse_args()
        lesson = database_test.ClassModel(args["number"], args["name"], 4.0, "*", "E301", "1-16", "None,AB,None,None,None,None,None",
                                          2015, 2016, 1)
        return ret_vals_helper(database_test.insert_to_database, lesson, "succeed to add the class")
        # ret_vals = database_test.insert_to_database(lesson)
        # if ret_vals[0]:
        #     return output_json(dict(status="succeed to add the class"), 200)
        # else:
        #     return output_json(dict(ERROR=ret_vals[1]), 0)

    def delete(self, name=""):
        if name == "":
            abort(404)
        lesson = database_test.ClassModel.query.filter_by(class_name=name).first()
        if lesson is not None:
            return ret_vals_helper(database_test.delete_from_database, lesson, "succeed to remove the class")
            # ret_vals = database_test.delete_from_database(lesson)
            # if ret_vals[0]:
            #     return output_json(dict(status="succeed to remove the lesson"), 200)
            # else:
            #     return output_json(dict(ERROR=ret_vals[1]), 0)
        else:
            abort(404)

api.add_resource(Cource, "/course", "/course/<name>")

class User(Resource):
    """
    用户
    """
    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("username", required=True)
        args = self.parser.parse_args()
        user = database_test.UserModel(args['username'])
        return ret_vals_helper(database_test.insert_to_database, user, "succeed to add the user")
        # ret_vals = database_test.insert_to_database(user)
        # if ret_vals[0]:
        #     return output_json(dict(user=repr(user)), 200)
        # else:
        #     return output_json(dict(ERROR=ret_vals[1]), 0)

    def delete(self, name=""):
        if name == "":
            abort(404)
        user = database_test.UserModel.query.filter_by(user_account=name).first()
        if user is None:
            return output_json(dict(ERROR="No such user"), 0)
        else:
            return ret_vals_helper(database_test.delete_from_database, user, "succeed to remove the user")
            # ret_vals = database_test.delete_from_database(user)
            # if ret_vals[0]:
            #     return output_json(dict(status="succeed to delete the user"), 200)
            # else:
            #     return output_json(dict(ERROR=ret_vals[1]))

api.add_resource(User, "/user", "/user/<name>")


class Homework(Resource):
    """
    发布作业信息
    """
    # publisher, pub_time, hand_in_time, content, lesson

    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("publisher", required=True)
        self.parser.add_argument("pub_time", required=True, type=float)
        self.parser.add_argument("hand_in_time", required=True, type=float)
        self.parser.add_argument("content", required=True)
        self.parser.add_argument("class_name", required=True)
        args = self.parser.parse_args()
        from datetime import datetime
        user = database_test.UserModel.query.filter_by(user_account=args['publisher']).first()
        if user is None:
            return output_json(dict(ERROR="no such user"), 0)
        lesson = database_test.ClassModel.query.filter_by(class_name=args['class_name']).first()
        if lesson is None:
            return output_json(dict(ERROR="no such class"), 0)
        homework = database_test.HomeworkModel(user, datetime.fromtimestamp(float(args['pub_time'])),
                                               datetime.fromtimestamp(float(args['hand_in_time'])), args['content'], lesson)
        return ret_vals_helper(database_test.insert_to_database, homework, "succeed to add the homework")


api.add_resource(Homework, "/homework")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)