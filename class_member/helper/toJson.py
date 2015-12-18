#!usr/bin/env python3
# -*- coding:utf-8 -*-

import re

# member_data = {}


def split_info(long_info, front, end):
    tmp = long_info.split(front)
    tmp = tmp[1].split(end)
    tmp = tmp[0]
    return tmp


def parse_class_members(file_info, no):
    member_data = dict()
    member_data['classNo'] = split_info(
        file_info, '<span id="ctl00_cpContent_lbl_ClassID">', '</span>')
    member_data['semester'] = split_info(
        file_info, '<span id="ctl00_cpContent_lbl_Semester">', '</span>')

    member_data['beginTime'] = split_info(
        file_info, '<span id="ctl00_cpContent_lbl_Time">', '</span>')

    member_data['className'] = split_info(
        file_info, '<span id="ctl00_cpContent_lbl_CourseName">', '</span>')

    member_data['teacherName'] = split_info(
        file_info, r'<a id="ctl00_cpContent_KkbTeacher" href="../Teacher/ClassTeacherInfo.aspx?ClassID=' + str(no) + r'" target="_blank">', '   ')

    member_data['classRoom'] = split_info(
        file_info, r'<a id="ctl00_cpContent_KkbClassroom" href="../ClassRoom/ClassClassroomInfo.aspx?ClassID=' + str(no) + r'" target="_blank">', '   ')

    stu = []

    file_info = file_info.split('ctl00_cpContent_gvStudent">')[1]

    pattern = re.compile(
        r'<tr class=.*?<td>(\d.*?\d)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td.*?</tr>', re.S)
    items = re.findall(pattern, file_info)
    for i in items:
        num = i[0].split('<td>')
        num = num[len(num) - 1]
        # print num,
        # i[1],
        # i[3]
        stu.append(dict(number=num, name=i[1], gender=i[2].split(' ')[
                   0], major=i[3].split(' ')[0],))

    member_data['stuNum'] = len(stu)
    member_data['student'] = stu
    # print(stu)
    return member_data


def to_json(raw_data, class_number):
    return parse_class_members(raw_data, class_number)
