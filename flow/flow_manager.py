# coding=utf-8
from .db_package.database_operation import *
from flask_restful import Resource, Api, abort, reqparse, output_json
from flask import request

from app import app
api = Api(app)


class UserQuery(Resource):
    """
    获取用户信息，默认不包含密码这项信息
    """
    def get(self, username=""):
        if username == "":
            users = get_all_users()
            if len(users) == 0:
                return output_json({"ERROR": "No user"}, 200)
            usernames = list(map(lambda x: x.username, users))
            return output_json({"users": usernames}, 200)
        user = get_user_by_name(username)
        if user:
            password = user.password
            if 'password' not in request.args or request.args['password'] != password:
                return output_json({"ERROR": "forbidden"}, 401)
            else:
                return output_json(user.to_simple_dict(), 200)
        else:
            abort(404, ERROR='no such user ' + username)

api.add_resource(UserQuery, "/user/<string:username>", "/user")



class UploadUser(Resource):
    """
    创建新的分享用户
    """
    parser = reqparse.RequestParser()
    def put(self):
        self.parser.add_argument("user", required=True)
        self.parser.add_argument("password", required=True)
        self.parser.add_argument("max_share", required=True)
        self.parser.add_argument("max_left", required=True)
        self.parser.add_argument("start", required=True)
        self.parser.add_argument("end", required=True)
        self.parser.add_argument("mac", required=True)
        args = self.parser.parse_args()
        user = User(args['user'], args['password'], args['start'], args['end'], args['max_share'],
                    args['max_left'], args['mac'])
        ret_vals = add_user(user)
        if ret_vals[0]:
            print_all_users(get_all_users())
            return output_json({"message": "okay"}, 201)
        else:
            print(ret_vals[1])
            return output_json({"ERROR": "failed"}, 409)

api.add_resource(UploadUser, "/adduser")


class AddShared(Resource):
    parser = reqparse.RequestParser()
    def put(self):
        # 获取者的
        self.parser.add_argument('given', required=True)
        # 分享者的
        self.parser.add_argument('give', required=True)
        self.parser.add_argument('count', required=True)
        self.parser.add_argument('left_flow', required=True)    # 更新分享者所剩下的流量
        args = self.parser.parse_args()
        if add_shared(args['give'], args['given'], args['count']):
            return output_json({}, 201)
        else:
            return output_json({"ERROR": "FALIED TO ADD"}, 401)

api.add_resource(AddShared, "/addshared")



