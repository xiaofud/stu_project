# coding=utf-8
import urllib
import urllib.request
from .oa_parser import parse

# CONSTANTS
UPDATED_ADDR = 'http://notes.stu.edu.cn/login/Login.jsp?logintype=1'    # 显示最新消息的页面
WEBSITE_ENCODING = 'GBK'
NOTIFICATION_COUNT = 10

def get_most_updated():
    resp = urllib.request.urlopen(UPDATED_ADDR)
    content = resp.read().decode(WEBSITE_ENCODING)
    return parse(content, count=NOTIFICATION_COUNT)


if __name__ == "__main__":
    messages = get_most_updated()
    for msg in messages:
        print(msg.to_dict())