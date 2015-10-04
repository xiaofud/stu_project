# coding=utf-8
import time
import sys, os
sys.path.append(os.path.abspath('..'))
from server import app
from db_package.database_operation import *
from flask_restful import Resource, Api, abort, reqparse, output_json

api = Api(app)


class UserQuery(Resource):
    """
    获取用户信息，默认不包含密码这项信息
    """
    def get(self, username=""):
        if username == "":
            users = get_all_users()
            usernames = list(map(lambda x: x.to_dict(), users))
            return output_json({"users": usernames}, 200)
        user = get_user_by_name(username)
        if user:
            return output_json(user.to_dict(), 200)
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
        args = self.parser.parse_args()
        user = User(args['user'], args['password'], args['start'], args['end'], args['max_share'],
                    args['max_left'])
        ret_vals = add_user(user)
        if ret_vals[0]:
            return output_json({"message": "okay"}, 201)
        else:
            return output_json({"ERROR": ret_vals[1]}, 409)

api.add_resource(UploadUser, "/adduser")


def test():
    nwad = User('14xfdeng', '123456', time.time(), time.time() + 3600 * 12, 100, 90)
    hj = User('Hj', '12323', time.time(), time.time() + 3600 * 6, 200, 100)
    add_user(nwad)
    add_user(hj)

    users = get_all_users_order_by_left_flow()
    print_all_users(users)

if __name__ == "__main__":
    test()
    app.run(debug=True)

