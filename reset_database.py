# coding=utf-8

"""
重置数据库的一些状态
"""

from class_interaction import database_models
# from . import database_models

def reset_nickname():
    """
    重置昵称到username
    :return:
    """
    users = database_models.UserModel.query.all()
    for user in users:
        user.user_nickname = user.user_account
    # 提交修改
    database_models.db.session.commit()

if __name__ == "__main__":
    reset_nickname()