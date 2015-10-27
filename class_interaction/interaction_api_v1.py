# coding=utf-8
# api的第一个版本
import time
from datetime import datetime
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

    delete_parser = reqparse.RequestParser()

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
        # from datetime import datetime
        # print(args['pub_time'])
        # print(datetime.now().timestamp())
        homework = database_test.HomeworkModel(user, datetime.fromtimestamp(time.time()),
                                               args['hand_in_time'], args['content'], lesson)
        # return ret_vals_helper(database_test.insert_to_database, homework, "succeed to add the homework")
        ret_vals = ret_vals_helper(database_test.insert_to_database, homework, "", False)
        if ret_vals[0]:
            # 返回 homework 在表中的主键
            return jsonify(status=homework.id)
        else:
            return jsonify(ERROR=ret_vals[1])

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



        discussion = database_test.DiscussModel(user, args["content"], datetime.fromtimestamp(time.time()), lesson)
        # return ret_vals_helper(database_test.insert_to_database, discussion, "succeed to add the discussion")
        ret_vals = ret_vals_helper(database_test.insert_to_database, discussion, "", False)
        if ret_vals[0]:
            # 返回 discussion 在表中的主键
            return jsonify(status=discussion.id)
        else:
            return jsonify(ERROR=ret_vals[1])

api.add_resource(DiscussionV1, "/api/v1.0/discuss")

class DeleteResource(Resource):

    delete_parser = reqparse.RequestParser()
    # <int:type_>  取值为 0(代表作业信息) 1(代表讨论信息)
    TYPE_HOMEWORK = 0
    TYPE_DISCUSSION = 1

    def delete(self, type_):
        # 删除信息
        # 在数据库里面的主键
        self.delete_parser.add_argument("resource_id", type=int, required=True)
        # 用户名，要匹配发布者，或者管理员
        self.delete_parser.add_argument("user", required=True)
        # 用户的token
        self.delete_parser.add_argument("token", required=True)

        args = self.delete_parser.parse_args()

        model = None
        # 先获取这个资源
        # 删除作业
        if type_ == DeleteResource.TYPE_HOMEWORK:
            model = database_test.HomeworkModel
        elif type_ == DeleteResource.TYPE_DISCUSSION:
            model = database_test.DiscussModel

        resource = database_test.query_by_id(model, args['resource_id'])
        if resource is None:
            return jsonify(ERROR="no such resource")

        # 检查用户
        request_user = args['user']
        user = database_test.query_user_by_name(request_user)
        if user is None:
            return jsonify(ERROR="no such user")
        # 普通用户没有权限删除其他人的信息
        if user != resource.user and user.user_account not in database_test.ADMINS:
            return jsonify(ERROR="not authorized: no such user or user not match")
        # token不匹配
        if args['token'] != user.user_certificate:
            print(user.user_certificate)
            return jsonify(ERROR="not authorized: wrong token")

        # 尝试删除
        ret_vals = database_test.delete_from_database(resource)
        if ret_vals[0]:
            return jsonify(status="deleted")
        else:
            return jsonify(ERROR=ret_vals[1])

api.add_resource(DeleteResource, "/api/v1.0/delete/<int:type_>")