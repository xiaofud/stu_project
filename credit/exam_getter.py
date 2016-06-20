# coding = utf-8
"""
    用于获取考试的原始数据
"""

from . import login_credit, exam_parser
from .error_string import *

# 1(秋季学期) 2(春季学期) 3(夏季学期)
AUTUMN = 1
SPRING = 2
SUMMER = 3

def get_exam_raw_data(username, password, start_year=2014, end_year=2015, semester=1, timeout=10):
    """
    获取考试信息的原始数据
    :param username:    用户名
    :param password:    密码
    :param start_year:       学年起始
    :param end_year:        学年结束
    :param semester:    学期(用数字表示)
    :param timeout:     超时时间
    :return: True, raw_data; False, error_code
    """

    ret_val = login_credit.login_credit(username, password, timeout=timeout)
    if not ret_val[0]:
        # 包括了 False 以及错误编号
        return ret_val
    else:
        # 用于打开学分制相应系统
        opener = ret_val[1]
    # print("got", username, password)
    url_encode_post_data = "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTIxMjE5NjM3MTQPFgIeAVgUKwADCylyQ3JlZGl0LkNvbW1vbi5EYXRhLkV4YW1EYXRhK1F1ZXJ5VHlwZSwgQ3JlZGl0LkNvbW1vbiwgVmVyc2lvbj02LjAuNTY2NS4xNjYyNSwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsAQUKMjAxNDEwMTA1OWYWAmYPZBYCAgMPZBYEAgMPZBYCAgEPZBYEZg8QDxYCHgRUZXh0BQ8yMDE0LTIwMTXlrablubRkEBUHDzIwMTEtMjAxMuWtpuW5tA8yMDEyLTIwMTPlrablubQPMjAxMy0yMDE05a2m5bm0DzIwMTQtMjAxNeWtpuW5tA8yMDE1LTIwMTblrablubQPMjAxNi0yMDE35a2m5bm0DzIwMTctMjAxOOWtpuW5tBUHDzIwMTEtMjAxMuWtpuW5tA8yMDEyLTIwMTPlrablubQPMjAxMy0yMDE05a2m5bm0DzIwMTQtMjAxNeWtpuW5tA8yMDE1LTIwMTblrablubQPMjAxNi0yMDE35a2m5bm0DzIwMTctMjAxOOWtpuW5tBQrAwdnZ2dnZ2dnFgBkAgEPEGRkFgECAmQCBw9kFgICAQ9kFgJmD2QWBGYPDxYCHwEFWDxCPuWQhOS4quWtpuW5tFsyMDE0MTAxMDU5XemCk%2BaZk%2BaLgiAg6K6h566X5py656eR5a2m5LiO5oqA5pyvKDIwMTQpPC9CPueahOiAg%2BivleS%2FoeaBrzpkZAIBDzwrAA0BAA8WBB4LXyFEYXRhQm91bmRnHgtfIUl0ZW1Db3VudGZkZBgDBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUXY3RsMDAkTVBDb25kaXRpb24kWVMkWE4FFmN0bDAwJE1QQ29udGVudCRtdkluZm8PD2QCAWQFGWN0bDAwJE1QQ29udGVudCRndlJlc3VsdHMPPCsACgEIZmRj97r%2Faut9ZPV6e81rs7zyJfjiog%3D%3D&__VIEWSTATEGENERATOR=B48389E8&__EVENTVALIDATION=%2FwEWDwKco9c1ApXN01EC0oL3rAQC0YLr6QUC2IKvuQcC14LD9wQCsbuhLAKwu9XqAQK3u5m6AwKHlpHQCwKElpHQCwKGlpHQCwKlzoroBQLf2diGCwK2%2BYezC91t3trIOZkV1BcWO20fwX5pHNxW&ctl00%24MPCondition%24YS%24XN%24Text=2014-2015%D1%A7%C4%EA&ctl00%24MPCondition%24YS%24XQ=1&ctl00%24MPCondition%24YS%24hfXN=&ctl00%24MPCondition%24btnQuery=%B2%E9%D1%AF"
    year_str = str(start_year) + "-" + str(end_year)
    url_encode_post_data = url_encode_post_data.replace("2014-2015", year_str)
    url_encode_post_data = url_encode_post_data.replace("XQ=1", "XQ=" + str(semester))

    url_encode_post_data = url_encode_post_data.encode()
    resp = opener.open("http://credit2.stu.edu.cn/Exam/ExmStudent.aspx", url_encode_post_data, timeout=timeout)
    return True, resp.read().decode(login_credit.WEBSITE_ENCODING)


def get_exam_list(username, password, start_year=2014, end_year=2015, semester=1, timeout=10):
    """
    获取考试信息
    :param username:
    :param password:
    :return:
    """
    ret_val = get_exam_raw_data(username, password, start_year, end_year, semester, timeout)
    if not ret_val[0]:
        return ret_val
    raw_data = ret_val[1]
    assert isinstance(raw_data, str)
    # 取出需要的部分
    start_str = "<tr class=\"DGItemStyle\">"
    start_index = raw_data.find(start_str)
    if start_index == -1:
        # print("nothing about the exams")
        return False, NO_EXAMS
    start_index += len(start_str)
    end_str = "</table>"
    end_index = raw_data.find(end_str, start_index)
    exam_str = raw_data[start_index: end_index]
    parser = exam_parser.ExamParser()
    return True, parser.get_exam_list(exam_str)



