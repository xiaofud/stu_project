# coding = utf-8

from credit import grade_getter
import json

if __name__ == "__main__":
    ret_val = grade_getter.get_grades_raw_data("14xfdeng", "Smallfly2nd")
    if ret_val[0]:
        raw_data = ret_val[1]
        grade_list, gpa = grade_getter.parse_grades(raw_data)
        print(grade_list)
        # print(gpa)


