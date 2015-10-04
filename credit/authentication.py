# coding=utf-8
# 借用学分制判断用户名与密码是否匹配
import urllib
import urllib.request
import socket

HOSTADDR = 'http://credit.stu.edu.cn/portal/stulogin.aspx'
WEBSITE_ENCODING = 'gbk'
MAX_TIME = 3  # 3 seconds

CORRECT = 0
INCORRECT = 1
TIMEDOUT = 2

def authenticate_by_credit(username, password):

    postdata = urllib.parse.urlencode({
        "txtUserID": username,
        "txtUserPwd": password,
        "btnLogon": "登录",
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '/wEPDwUKMTM1MzI1Njg5N2Rk47x7/EAaT/4MwkLGxreXh8mHHxA=',
        '__VIEWSTATEGENERATOR': 'FBAF4793',
        '__EVENTVALIDATION': '/wEWBAKo25zdBALT8dy8BQLG8eCkDwKk07qFCRXt1F3RFYVdjuYasktKIhLnziqd'
    })
    postdata = postdata.encode("utf-8")

    try:
        resp = urllib.request.urlopen(HOSTADDR, postdata, timeout=MAX_TIME)
    except socket.timeout:
        return TIMEDOUT
    content = resp.read()
    if content.__contains__(b'alert'):
        return INCORRECT
    else:
        return CORRECT

def test_it(user, passwd):
    code = authenticate_by_credit(user, passwd)
    if code == INCORRECT:
        print("wrong")
    elif code == CORRECT:
        print("right")
    elif code == TIMEDOUT:
        print("time out")

if __name__ == "__main__":
    test_it("14xfdeng", "Smallfly2nd")
    test_it("14xfdeng", "haha")