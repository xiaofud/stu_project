# coding = utf-8

from .login_credit import login_credit, WEBSITE_ENCODING, _GLOBAL_DEFAULT_TIMEOUT

def get_grades(username, password, timeout=_GLOBAL_DEFAULT_TIMEOUT):
    ret_val = login_credit(username, password, timeout)
    if ret_val[0]:
        opener = ret_val[1]
    else:
        return ret_val

    resp = opener.open("http://credit.stu.edu.cn/Grade/MyGradeStudent.aspx", timeout=timeout)
    return resp.read().decode(WEBSITE_ENCODING)