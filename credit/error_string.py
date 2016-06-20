# coding = utf-8

"""
    把错误常量转化位字符串
"""

EMPTY_DATA = 0
WRONG_SEMESTER = 1
WRONG_PASSWORD = 2
WRONG_DATE = 3
TIME_OUT = 4
SYSTEM_BROKEN = 5
NOT_ALLOWED = 6

NO_EXAMS = 7

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
    elif code == NO_EXAMS:
        return "no exams"
    else:
        return "UNKNOWN"