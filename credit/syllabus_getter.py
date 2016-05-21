# coding = utf-8

"""
    用于获取 课表信息
"""
import os
from socket import _GLOBAL_DEFAULT_TIMEOUT
from .login_credit import login_credit
from . import class_info_parser
from . import error_string


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
            return False, error_string.WRONG_SEMESTER

        # if user.strip() == "" or passwd.strip() == "":
        #     return False, EMPTY_DATA

        if not isinstance(start_year, int) or not isinstance(end_year, int) or end_year <= start_year:
            return False, error_string.WRONG_DATE

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
        return False, error_string.TIME_OUT

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

def parse(content):
    parser = class_info_parser.ClassParser()
    content = class_info_parser.get_class_html_parts(content)
    lesson_list = list()
    for lesson in content:
        # 一个奇怪的BUG
        # 在本机上运行OK
        # 但在服务器的python版本上不这样的话会出现问题
        # 在服务器上需要 replace
        parser.feed(lesson.replace("&", "and"))
        lesson_list.append(parser.lesson)
        parser.clear()  # 记得每次都需要clear一次，不然返回的数据是第一次的数据
    parser.close()
    return lesson_list

if __name__ == "__main__":
    ret_val = get_syllabus("14xfdeng", "Smallfly2nd", start_year=2014, end_year=2015, semester=AUTUMN)
    if ret_val[0]:
        source = ret_val[1]
        lessons = parse(source.decode("UTF-8"))     # 学校的那个网站用的是GBK编码，有点坑爹
        print(class_info_parser.Lesson.jsonfy_all(lessons))
    else:
        print(ret_val[1])