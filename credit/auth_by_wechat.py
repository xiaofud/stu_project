# coding=utf-8
__author__ = 'smallfly'

ADDRESS = "http://wechat.stu.edu.cn/wechat/login/login_verify"

import urllib
import urllib.request
import urllib.parse

def auth(username, password):
    """
    使用微信方式验证
    :param username:    帐号名
    :param password:    密码
    :return:    True, 账号密码匹配 False 账号密码不匹配 None 网络错误
    """
    # print(username, password)
    post_data = {
        "ldap_account": username,
        "ldap_password": password,
        "btn_ok": "登录",
        "source_type": "",
        "openid": ""
    }
    post_data = urllib.parse.urlencode(post_data)
    post_data = post_data.encode("utf-8")
    request = urllib.request.Request(ADDRESS, data=post_data, method="POST")
    try:
        resp = urllib.request.urlopen(request, timeout=5)
        print(resp.getcode())
        content = resp.read().decode("utf-8")
        if "账号或者密码错误" in content:
            print("error password in wechat auth")
            return False
        print("correct password in wechat auth")
        return True
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    print(auth("test", ""))