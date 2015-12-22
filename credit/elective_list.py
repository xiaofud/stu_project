# coding = utf-8
"""
获取已选课程
"""

from . import login_credit
from . import error_string

TARGET_ADDRESS = "http://credit.stu.edu.cn/Elective/MyElectiveList.aspx"
WEBSITE_ENCODING = "GBK"

def get_html_source(username, password, timeout=7):
    ret_val = login_credit.login_credit(username, password, timeout)
    if not ret_val[0]:
        return ret_val
    # 获取成功
    opener = ret_val[1]
    try:
        resp = opener.open(TARGET_ADDRESS, timeout=timeout)
        return True, resp.read().decode(WEBSITE_ENCODING)
    except Exception as err:
        print(type(err), err)
        return False, error_string.TIME_OUT
