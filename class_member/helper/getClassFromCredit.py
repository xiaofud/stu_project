#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request

WEBSITE_ENCODING = "GBK"
TIME_OUT = 4 # 4s

def getClassByClassNo(classNo):
    url = 'http://credit2.stu.edu.cn/Info/DisplayKkb.aspx?ClassID=' + str(classNo)
    try:
        content = urllib.request.urlopen(url, timeout=TIME_OUT).read().decode(WEBSITE_ENCODING)
        return content
    except Exception as err:
        print(type(err), err)
        return None


def main():
    # 81229 电工电子
    #80927是开课班号
    print(getClassByClassNo(80927))

if __name__ == '__main__':
    raw_data = getClassByClassNo(81229)
    with open("class_member.txt", "w") as f:
        f.write(raw_data)

