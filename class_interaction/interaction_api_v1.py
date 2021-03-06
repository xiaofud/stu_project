# coding=utf-8
# api的第一个版本
import time
from datetime import datetime
from .interaction_api import *
from oa import oa_main
from class_member import class_members_getter
from helpers.date_helper import week_manager
from notification import notification_manager

def check_token(username, token):
    user = database_models.UserModel.query.filter_by(user_account=username).first()
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

        user = database_models.UserModel.query.filter_by(user_account=args['publisher']).first()
        if user is None:
            return jsonify(ERROR="no such user")
        class_id = str(args['start_year']) + "_" + str(args["end_year"]) + "_" + str(args['semester']) + "_" + str(args['number'])
        lesson = database_models.ClassModel.query.filter_by(class_id=class_id).first()
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
        homework = database_models.HomeworkModel(user, datetime.fromtimestamp(time.time()),
                                               args['hand_in_time'], args['content'], lesson)
        # return ret_vals_helper(database_test.insert_to_database, homework, "succeed to add the homework")
        ret_vals = ret_vals_helper(database_models.insert_to_database, homework, "", False)
        if ret_vals[0]:
            # 返回 homework 在表中的主键
            return jsonify(status=homework.id, nickname=user.user_nickname)
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
        user = database_models.UserModel.query.filter_by(user_account=args['publisher']).first()
        if user is None:
            return jsonify(ERROR="no such user")
        class_id = str(args['start_year']) + "_" + str(args["end_year"]) + "_" + str(args['semester']) + "_" + str(args['number'])
        lesson = database_models.ClassModel.query.filter_by(class_id=class_id).first()
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



        discussion = database_models.DiscussModel(user, args["content"], datetime.fromtimestamp(time.time()), lesson)
        # return ret_vals_helper(database_test.insert_to_database, discussion, "succeed to add the discussion")
        ret_vals = ret_vals_helper(database_models.insert_to_database, discussion, "", False)
        if ret_vals[0]:
            # 返回 discussion 在表中的主键
            return jsonify(status=discussion.id, nickname=user.user_nickname)
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
            model = database_models.HomeworkModel
        elif type_ == DeleteResource.TYPE_DISCUSSION:
            model = database_models.DiscussModel

        resource = database_models.query_by_id(model, args['resource_id'])
        if resource is None:
            return jsonify(ERROR="no such resource")

        # 检查用户
        request_user = args['user']
        user = database_models.query_user_by_school_account(request_user)
        if user is None:
            return jsonify(ERROR="no such user")
        # 普通用户没有权限删除其他人的信息
        if user != resource.user and user.user_account not in database_models.ADMINS:
            return jsonify(ERROR="not authorized: no such user or user not match")
        # token不匹配
        if args['token'] != user.user_certificate:
            print(user.user_certificate)
            return jsonify(ERROR="not authorized: wrong token")

        # 尝试删除
        ret_vals = database_models.delete_from_database(resource)
        if ret_vals[0]:
            return jsonify(status="deleted")
        else:
            return jsonify(ERROR=ret_vals[1])

api.add_resource(DeleteResource, "/api/v1.0/delete/<int:type_>")

class ModifyUser(Resource):
    """
    修改用户信息
    """
    parser = reqparse.RequestParser()

    # post 和 put 都可以
    def post(self):
        return self.put()

    def put(self):
        """
        更新用户信息
        """
        # 用户名 14xfdeng
        self.parser.add_argument("username", required=True)
        self.parser.add_argument("token", required=True)
        # 昵称
        self.parser.add_argument("nickname")
        self.parser.add_argument("birthday", type=float)

        args = self.parser.parse_args()
        username = args['username']
        token = args['token']

        nickname = args.get("nickname", None)
        birthday = args.get("birthday", None)


        # 在数据库中查找用户
        user = database_models.query_user_by_school_account(username)
        if user is None:
            return jsonify(ERROR="no such user")
        if token != user.user_certificate:
            return jsonify(ERROR="wrong token")


        if nickname is not None:
            assert isinstance(nickname, str)
            if len(nickname) > 20:
                return jsonify(ERROR="nickname too long")

            if len(nickname.strip()) < 2:
                return jsonify(ERROR="nickname too short, at least 2")

            if len(nickname.strip()) == 0:
                return jsonify(ERROR="empty name")

            # 检查是否有人同名
            user_who_has_the_same_nickname = database_models.query_user_by_nickname(nickname)
            # 不允许同名, 但是是自己的话就无所谓
            if user_who_has_the_same_nickname is not None and \
                user_who_has_the_same_nickname != user:
                return jsonify(ERROR="the nickname has been used")
            # 不允许其他用户使用数据库里面存在的帐号名, 比如说 14xfdeng 和 14jhwang 都在数据库内
            # 那么 对于 nickname 14xfdeng, 只允许 14xfdeng 这个账号拥有
            # 判断 这个 nickname 是不是数据库中某个账号名
            nickname_is_the_account_user = database_models.query_user_by_school_account(nickname)
            # 如果数据库存在这个账号
            if nickname_is_the_account_user is not None and \
                user.user_account != nickname_is_the_account_user.user_account:
                    return jsonify(ERROR="not authorized to use this name")

            # 保存去掉首尾空格的名称
            user.user_nickname = nickname.strip()
        if birthday is not None:
            user.user_birthday = datetime.fromtimestamp(float(birthday))

        # 提交修改到数据库中
        ret_val = database_models.commit()
        if ret_val[0]:
            return jsonify(status="okay")
        else:
            return jsonify(ERROR=ret_val[1])

api.add_resource(ModifyUser, "/api/v1.0/modify_user")


class OAResource(Resource):

    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("url", required=True)

        args = self.parser.parse_args()
        url = args['url']
        # return oa_main.send_out_oa_page(url)
        ret_val = oa_main.send_out_oa_page(url)
        if ret_val[0]:
            return ret_val[1]
        else:
            return jsonify(ERROR="time out")

    def get(self):
        test_url = "http://notes.stu.edu.cn/page/maint/template/news/newstemplateprotal.jsp?templatetype=1&templateid=3&docid=4974"
        return oa_main.send_out_oa_page(test_url)

api.add_resource(OAResource, "/api/v1.0/oa")

class Members(Resource):

    def __init__(self):
        super(Members, self).__init__()
        self.parser = reqparse.RequestParser()
        # query string
        self.parser.add_argument("class_id", required=True, location="args")

    def get(self):
        args = self.parser.parse_args()
        class_id = args['class_id']
        member_dict = class_members_getter.get(class_id)
        if member_dict is not None:
            return jsonify(class_info=class_members_getter.get(class_id))
        else:
            return jsonify(ERROR="error")

api.add_resource(Members, "/api/v1.0/member")

class UserCount(Resource):
    """
    返回现有的用户量
    """

    def get(self):
        last_user = database_models.get_last_inserted_record(database_models.UserModel)
        if last_user is not None:
            return jsonify(user_count=last_user.id)
        else:
            return  jsonify(user_count=0)

api.add_resource(UserCount, "/api/v1.0/user_count")

class SchoolWeek(Resource):
    """
    返回当前的周数
    testing: curl localhost:6000/api/v1.0/week?date=2016/3/19
    """

    def __init__(self):
        super(SchoolWeek, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("date")

    def get(self):
        args = self.parser.parse_args()
        check_date = datetime.now().date()
        if args["date"] is not None:
            try:
                check_date = datetime.strptime(args["date"], "%Y/%m/%d").date()
            except Exception as e:
                print(e)
                return jsonify(ERROR="date format: %Y/%m/%d")

        week = week_manager.calculate_week(check_date, week_manager.DEFAULT_FILE_PATH)
        return jsonify(week=week)

api.add_resource(SchoolWeek, "/api/v1.0/week")


class Notification(Resource):
    """
    返回最新的通知数据
    """
    def get(self):
        obj = notification_manager.get_notification()
        if obj is not None:
            return jsonify(latest=obj)
        else:
            return jsonify(ERROR="no any notifications")

api.add_resource(Notification, "/api/v1.0/notification", "/api/v1.0/notification/")

# class Broadcast(Resource):
#     """
#         用于在所有课程上广播(公共聊天区域)
#     """
#     pass