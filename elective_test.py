# coding=utf-8

from credit.elective_list import get_html_source, error_string

if __name__ == "__main__":
    ret_val = get_html_source("14xfdeng", "wrongpassword")
    if ret_val[0]:
        print(ret_val[1])
    else:
        print(error_string.err_srt(ret_val[1]))
