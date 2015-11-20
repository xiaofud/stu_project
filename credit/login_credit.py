# -*- coding: utf-8 -*-
import urllib
import urllib.request
import http.client
import http.cookiejar
from socket import _GLOBAL_DEFAULT_TIMEOUT
from . import get_course_info
# import get_course_info
import os


HOSTADDR = 'http://credit.stu.edu.cn/portal/stulogin.aspx'
# 1(秋季学期) 2(春季学期) 3(夏季学期)
AUTUMN = 1
SPRING = 2
SUMMER = 3

WEBSITE_ENCODING = 'gbk'

# 是否缓存课程表
CACHE_SYLLABUS = False
# 保存缓存文件的目录
DIR_NAME = "syllabus_dir"
CACHE_DIR = os.path.join(os.path.dirname(__file__), DIR_NAME)

# 错误常量
EMPTY_DATA = 0
WRONG_SEMESTER = 1
WRONG_PASSWORD = 2
WRONG_DATE = 3
TIME_OUT = 4
SYSTEM_BROKEN = 5
NOT_ALLOWED = 6

def err_srt(code):
    if code == EMPTY_DATA:
        return "username and password can't be empty"
    elif code == WRONG_SEMESTER:
        return "semester must be one of AUTUMN, SPRING, SUMMER"
    elif code == WRONG_PASSWORD:
        return "the password is wrong"
    elif code == WRONG_DATE:
        return "the date is wrong"
    elif code == TIME_OUT:
        return "timeout"
    elif code == SYSTEM_BROKEN:
        return "credit system broken"
    elif code == NOT_ALLOWED:
        return "account not exist or not allowed"

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
        resp = opener.open(HOSTADDR, post_data, timeout=timeout)
        # 登录后的情况
        content = resp.read()
        wrong_password = "认证服务器密码错误".encode(WEBSITE_ENCODING)
        if content.__contains__(wrong_password):
            return False, WRONG_PASSWORD
        # 该账号不存在或者不允许被使用学分制系统
        elif content.__contains__(b'not allowed to access this system'):
            return False, NOT_ALLOWED
        elif content.__contains__(b'alert'):    # 提示欠费那个错误
            return False, SYSTEM_BROKEN

        return True, opener

    except Exception as err:
        print(type(err), str(err))
        return False, TIME_OUT

def get_syllabus(username, password, start_year=2015, end_year=2016, semester=AUTUMN, timeout=_GLOBAL_DEFAULT_TIMEOUT):
    """
    登录学分制网站
    :param username:
    :param password:
    :param semester: 可选的值有 AUTUMN = 1 SPRING = 2 SUMMER = 3
    :return:
    """
    try:
        # 对参数进行检查
        if semester not in (AUTUMN, SPRING, SUMMER):
            return False, WRONG_SEMESTER

        # if user.strip() == "" or passwd.strip() == "":
        #     return False, EMPTY_DATA

        if not isinstance(start_year, int) or not isinstance(end_year, int) or end_year <= start_year:
            return False, WRONG_DATE

        ret_val = login_credit(username, password, timeout)
        if ret_val[0]:
            opener = ret_val[1]
        else:
            return ret_val

        # 查看课表
        resp = opener.open('http://credit.stu.edu.cn/Elective/MyCurriculumSchedule.aspx', timeout=timeout)
        content = resp.read()
        assert isinstance(content, bytes)
        start_str = b'.aspx?'
        start_index = content.find(start_str)
        end_index = content.find(b' ', start_index)
        args = content[start_index + len(start_str): end_index - 1]
        # print(type(args))
        curriculum_url = (b'http://credit.stu.edu.cn/Student/StudentTimeTable.aspx?' + args).decode(WEBSITE_ENCODING)
        # print(curriculum_url)
        data =('__EVENTTARGET=&__EVENTARGUMENT=' \
              '&__VIEWSTATE=%2FwEPDwUKLTc4MzA3NjE3Mg9kFgICAQ9kFgYCAQ9kFgRmDxAPFgIeBFRleHQFDzIwMTUtMjAxNuWtpuW5tGQQFQcPMjAxMi0yMDEz5a2m5bm0DzIwMTMtMjAxNOWtpuW5tA8yMDE0LTIwMTXlrablubQPMjAxNS0yMDE25a2m5bm0DzIwMTYtMjAxN%2BWtpuW5tA8yMDE3LTIwMTjlrablubQPMjAxOC0yMDE55a2m5bm0FQc' \
              'PMjAxMi0yMDEz5a2m5bm0DzIwMTMtMjAxNOWtpuW5tA8yMDE0LTIwMTXlrablubQPMjAxNS0yMDE25a2m' \
              '5bm0DzIwMTYtMjAxN%2BWtpuW5tA8yMDE3LTIwMTjlrablubQPMjAxOC0yMDE55a2m' \
              '5bm0FCsDB2dnZ2dnZ2cWAGQCAQ8QZGQWAQICZAIFDxQrAAsP' \
              'FggeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50Zh4JUGFnZUNvdW50Ag' \
              'EeFV8hRGF0YVNvdXJjZUl0ZW1Db3VudGZkZBYEHghDc3NDbGFzcwUMREdQYWdlclN0eWxlHgRfIVN' \
              'CAgIWBB8FBQ1ER0hlYWRlclN0eWxlHwYCAhYEHwUFDURHRm9vdGVyU3R5bGUfBgICFgQfBQULREdJdGVtU3R5bGUfBgICFgQfBQUWREdBbHRlcm5hdGluZ0l0ZW1TdHlsZR8GAgIWBB8FBRNER1NlbGVjdGVkSXRlbVN0eWxlHwYCAhYEHwUFD0RHRWRpdEl0ZW1TdHlsZR8GAgIWBB8FBQJERx8GAgJkFgJmD2QWAgIBD2QWBAIDDw8WAh8ABQ3lhbEw6Zeo6K' \
              '%2B%2B56iLZGQCBA8PFgIfAAUHMOWtpuWIhmRkAgYPFCsACw8WAh4HVmlzaWJsZWhkZBYEHwUFDERHUGFnZXJTdHlsZR8GAgIWBB8FBQ1ER0hlYWRlclN0eWxlHwYCAhYEHwUFDURHRm9vdGVyU3R5bGUfBgICFgQfBQULREdJdGVtU3R5bGUfBgICFgQfBQUWREdBbHRlcm5hdGluZ0l0ZW1TdHlsZR8GAgIWBB8FBRNER1NlbGVjdGVkSXRlbVN0eWxlHwYCAhYEHwUFD0RHRWRpdEl0ZW1TdHlsZR8GAgIWBB8FBQJERx8GAgJkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUIdWNzWVMkWE4FCWJ0blNlYXJjaIOA1hvkaeyr6hBNdPilFTCCDv8u' \
              '&__VIEWSTATEGENERATOR=E672B8C6&__EVENTVALIDATION=%2FwEWDgKP7Z%2FyDQKA2K7WDwKl3bLICQKs3faYCwKj3ZrWCALF5PiNDALE5IzLDQLD5MCbDwKv3YqZDQL7tY9IAvi1j0gC' \
              '%2BrWPSAL63YQMAqWf8%2B4KZKbR9XsGkypHcOunFkHTcdqR6to%3D&' \
              'ucsYS%24XN%24Text={}-{}%' \
              'D1%A7%C4%EA&ucsYS%24XQ=' + str(semester) + '&ucsYS%24hfXN=&btnSearch.x=42&btnSearch.y=21').format(start_year, end_year)
            # 'ucsYS%24XN%24Text=' + str(start_year) + '-' + str(end_year) + '%' \
                # 上面的Text那里是学年的选择，XQ 有三个取值 1(秋季学期) 2(春季学期) 3(夏季学期)
        # print(data)
        data = data.encode('utf-8')

        resp = opener.open(curriculum_url, data=data, timeout=timeout)
        content = resp.read()
        content = convert_encoding(content, "GBK", "UTF-8")
        # print("In login_credit", type(content))
        return True, content
    except Exception as err:
        print(type(err), str(err))
        return False, TIME_OUT

# 缓存课程文件, JSON 格式
def save_file(filename, data):
    if not os.path.exists(CACHE_DIR):
        try:
            original_umask = os.umask(0)
            os.mkdir(CACHE_DIR)
        finally:
            os.umask(original_umask)
    with open(os.path.join(CACHE_DIR, filename), "w", encoding="UTF-8") as f:
        print("saving " + filename)
        f.write(data)

def get_grades(username, password, timeout=_GLOBAL_DEFAULT_TIMEOUT):
    ret_val = login_credit(username, password, timeout)
    if ret_val[0]:
        opener = ret_val[1]
    else:
        return ret_val

    resp = opener.open("http://credit.stu.edu.cn/Grade/MyGradeStudent.aspx", timeout=timeout)
    return resp.read().decode(WEBSITE_ENCODING)


def parse(content):
    parser = get_course_info.ClassParser()
    content = get_course_info.get_class_html_parts(content)
    lessons = []
    for lesson in content:
        parser.feed(lesson)
        lessons.append(parser.lesson)
        parser.clear()  # 记得每次都需要clear一次，不然返回的数据是第一次的数据
    parser.close()
    return lessons

if __name__ == "__main__":
    # ret_val = get_syllabus("14xfdeng", "Smallfly2nd", start_year=2014, end_year=2015, semester=AUTUMN)
    # if ret_val[0]:
    #     source = ret_val[1]
    #     lessons = parse(source.decode("UTF-8"))     # 学校的那个网站用的是GBK编码，有点坑爹
    #     print(get_course_info.Lesson.jsonfy_all(lessons))
    # else:
    #     print(err_srt(ret_val[1]))
    print(get_grades("14xfdeng", "Smallfly2nd"))
