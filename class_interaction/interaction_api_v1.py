# coding=utf-8
# api的第一个版本
from .interaction_api import *
    # api, Resource, class_arg_parser_helper,\
    # database_test, jsonify, ret_vals_helper, reqparse

def check_token(username, token):
    user = database_test.UserModel.query.filter_by(user_account=username).first()
    if user is not None:
        print(user.user_account, user.user_certificate)
        if user.user_certificate == token:
            return True
    return False

class HomeworkV1(Resource):
    """
    发布作业信息 版本v1.0 加入token, 暂时取消hash_code
    """
    # publisher, pub_time, hand_in_time, content, lesson

    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("publisher", required=True)
        self.parser.add_argument("pub_time", required=True, type=float)
        self.parser.add_argument("hand_in_time", required=True)
        self.parser.add_argument("content", required=True)
        # self.parser.add_argument("code", required=True)  # hash_code
        self.parser.add_argument("token", required=True)

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
        # timestamp = str( int(args['pub_time']) )
        # hash_code = args["code"]
        # if not check_hash(hash_code, username+timestamp):
        #     return jsonify(ERROR="wrong code")
        user_token = str(args['token'])  # token
        if not check_token(username, user_token):
            return jsonify(ERROR="wrong token")
        from datetime import datetime
        # print(args['pub_time'])
        # print(datetime.now().timestamp())
        homework = database_test.HomeworkModel(user, datetime.fromtimestamp(float(args['pub_time'])),
                                               args['hand_in_time'], args['content'], lesson)
        return ret_vals_helper(database_test.insert_to_database, homework, "succeed to add the homework")

api.add_resource(HomeworkV1, "/api/v1.0/homework")

class DiscussionV1(Resource):
    """
    发布作业信息 v1.0 加入token 暂时去除hash_code
    """
    # def __init__(self, publisher, content, when, lesson):

    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("publisher", required=True)
        self.parser.add_argument("pub_time", required=True, type=float)
        self.parser.add_argument("content", required=True)
        self.parser.add_argument("token", required=True)
        # self.parser.add_argument("code", required=True)
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
        # timestamp = str( int(args["pub_time"]) )
        # hash_code = args["code"]
        # if not check_hash(hash_code, username+timestamp):
        #     return jsonify(ERROR="wrong code")

        user_token = str(args['token'])
        if not check_token(username, user_token):
            return jsonify(ERROR="wrong token")

        from datetime import datetime
        discussion = database_test.DiscussModel(user, args["content"], datetime.fromtimestamp(float(args['pub_time'])), lesson)
        return ret_vals_helper(database_test.insert_to_database, discussion, "succeed to add the discussion")


api.add_resource(DiscussionV1, "/api/v1.0/discuss")