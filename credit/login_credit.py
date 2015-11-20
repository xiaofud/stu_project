# -*- coding: utf-8 -*-
import urllib
import urllib.request
import http.client
import http.cookiejar
from socket import _GLOBAL_DEFAULT_TIMEOUT

from . import error_string

WEBSITE_ENCODING = 'gbk'

# 学分制的登陆地址
LOGIN_ADDRESS = 'http://credit.stu.edu.cn/portal/stulogin.aspx'

def convert_encoding(data, from_, to):
    """
    转换编码
    :param data : bytes
    :param from_: 原编码
    :param to:  转换后的编码
    :return: 转换编码后的数据, bytes
    """
    # print("in convert_encoding", type(data))
    # 用 之前的编码 解码成 str
    # 再用 需要转换的编码 编码成 bytes
    tmp = data.decode(from_).encode(to)

    return tmp

def login_credit(username, password, timeout=_GLOBAL_DEFAULT_TIMEOUT):
    """
        登陆学分制，返回相应的opener
    :param username:    用户名
    :param password:    密码
    :return:    True, opener; False, Error_Code
    """
    try:
        # 登录学分制需要POST的数据
        post_data = urllib.parse.urlencode({
            "txtUserID": username,
            "txtUserPwd": password,
            "btnLogon": "登录",
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUKMTM1MzI1Njg5N2Rk47x7/EAaT/4MwkLGxreXh8mHHxA=',
            '__VIEWSTATEGENERATOR': 'FBAF4793',
            '__EVENTVALIDATION': '/wEWBAKo25zdBALT8dy8BQLG8eCkDwKk07qFCRXt1F3RFYVdjuYasktKIhLnziqd'
        })
        # 需要转换为字节流
        post_data = post_data.encode("utf-8")
        cookie_jar = http.cookiejar.CookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookie_jar)
        opener = urllib.request.build_opener(handler)
        # 此处的open方法同urllib2的urlopen方法，也可以传入request
        resp = opener.open(LOGIN_ADDRESS, post_data, timeout=timeout)
        # 登录后的情况
        content = resp.read()
        wrong_password = "认证服务器密码错误".encode(WEBSITE_ENCODING)
        if content.__contains__(wrong_password):
            return False, error_string.WRONG_PASSWORD
        # 该账号不存在或者不允许被使用学分制系统
        elif content.__contains__(b'not allowed to access this system'):
            return False, error_string.NOT_ALLOWED
        elif content.__contains__(b'alert'):    # 提示欠费那个错误
            return False, error_string.SYSTEM_BROKEN

        return True, opener

    except Exception as err:
        print(type(err), str(err))
        return False, error_string.TIME_OUT



if __name__ == "__main__":
    ret_val = login_credit("xxx")
    if ret_val[0]:
        print("okay")
    else:
        print("oh shit", ret_val[1])
