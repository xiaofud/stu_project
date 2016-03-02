# coding=utf-8
import json
import os
import datetime

INITIAL_WEEK_FILENAME = "initial_week.txt"
DEFAULT_FILE_PATH = os.path.dirname(__file__) + str(os.path.sep) + INITIAL_WEEK_FILENAME

def update_initial_week(theDate, theWeek, filePath=DEFAULT_FILE_PATH):
    """
    更新周数文件
    :param theDate:
    :param theWeek:
    :return:
    """
    json_data = {
        "date": theDate,
        "week": theWeek
    }
    with open(filePath, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False)

def get_initial_data(filePath):
    with open(filePath, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_week(theDate, filePath):
    """
    从传入的date中获取第几周
    :param theDate: 输入的日期 是 datetime.datetime 里面的 date 对象
    :param filePath: 记录初始周的文件
    :return:
    """
    initial_data = get_initial_data(filePath)
    initial_date = datetime.datetime.strptime(initial_data["date"], "%Y/%m/%d").date()
    diff = theDate - initial_date
    # 整除
    passed_weeks = diff.days // 7
    return passed_weeks + initial_data["week"]

def set_initial_date():
    date = input("input date(y/m/d) ")
    week = input("the corresponding week ")
    week = int(week)
    update_initial_week(date, week)

if __name__ == "__main__":
    set_initial_date()