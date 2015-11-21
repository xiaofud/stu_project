# coding = utf-8

from .login_credit import login_credit, WEBSITE_ENCODING, _GLOBAL_DEFAULT_TIMEOUT
from . import error_string
from .grade_parser import GradeParser, Grade

def get_grades_raw_data(username, password, timeout=_GLOBAL_DEFAULT_TIMEOUT):
    """
        获取成绩的原始信息
    :param username:
    :param password:
    :param timeout:
    :return: False, error_code; True, 网页的原始内容
    """
    ret_val = login_credit(username, password, timeout)
    if ret_val[0]:
        opener = ret_val[1]
    else:
        return ret_val
    try:
        resp = opener.open("http://credit.stu.edu.cn/Grade/MyGradeStudent.aspx", timeout=timeout)
        return True, resp.read().decode(WEBSITE_ENCODING)
    except Exception as err:
        print(__file__, type(err), str(err))
        return False, error_string.TIME_OUT

def figure_gpa(grade_list):
    """
        计算GPA
    :param raw_data:    成绩单页面的原始HTML内容
    :param opener:  已经登陆学分制成功的 http_opener(带cookie)
    :return: GPA
    """
    assert isinstance(grade_list, list)
    if len(grade_list) == 0:
        return -1
    grade_sum = 0.0
    credit_sum = 0.0
    # length = len(grade_list)
    for semester_grade in grade_list:
        for grade in semester_grade:
            assert isinstance(grade, dict)
            # 加权
            grade_point = float(grade['class_grade']) - 50
            if grade_point < 60 - 50:
                # 即不及格的时候，这科的绩点为0
                grade_point = 0
            grade_sum += grade_point / 10 * float(grade['class_credit'])
            credit_sum += float(grade['class_credit'])
    return grade_sum  /  credit_sum


def parse_grades(raw_data):
    """
        处理原始数据，使得 grade_parser 可以解析
    :param raw_data:    网站的原始数据
    :return:    string_list 每个元素都是一个学期的课程
    """
    assert isinstance(raw_data, str)
    # year_count = raw_data.count("学年")
    # semester_count = raw_data.count("学期")
    # print("一共有", year_count, "个学年的成绩")
    # print("一共有", semester_count, "个学期的成绩")

    # 获取学年数据
    year_index = raw_data.find("学年")
    # print(year_index)

    grade_list = list()

    while year_index != -1:
    # if year_index != -1:
        # 在 raw_data的 [ year_index - 20, year_index] 这个范围内 反向查找 > 这个字符，注意
        # year_index - 20 的20并没有什么特殊意义，只是将范围合理地缩小了而已
        year_tag_index = raw_data.rfind(">", year_index - 20, year_index)
        cur_year_str = raw_data[year_tag_index + 1 :year_index]
        # print(cur_year_str)
        next_year_index = raw_data.find("学年", year_index + 4)
        if next_year_index != -1:
            semester_data = raw_data[year_index : next_year_index]
        else:
            semester_data = raw_data[year_index: ]
        # 开始定位学期
        semester_index = semester_data.find("学期")
        while semester_index != -1:
            cur_semester = semester_data[ semester_index - 2 : semester_index + 2]
            # print(cur_semester)

            # 定位这个学期的成绩单
            tmp_index = semester_data.find("学分", semester_index)
            grade_start_index = semester_data.find("<tr>", tmp_index)
            grade_end_index = semester_data.find("共", grade_start_index)
            grade_end_index = semester_data.find("</tr>", grade_end_index)
            grade_string = semester_data[grade_start_index : grade_end_index + len("</tr>")]
            parser = GradeParser(None, None)
            # print(parser.get_grades(grade_string, cur_year_str, cur_semester))
                                                                                        # 转化为字典，便于json化
            grade_list.append(parser.get_grades(grade_string, cur_year_str, cur_semester))


            semester_index = semester_data.find("学期", grade_end_index)

        year_index = raw_data.find("学年", year_index + 4)

    gpa = figure_gpa(grade_list)
    return grade_list, gpa



