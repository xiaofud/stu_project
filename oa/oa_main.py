# coding=utf-8
import urllib
import urllib.request
from .oa_parser import parse

# CONSTANTS
UPDATED_ADDR = 'http://notes.stu.edu.cn/login/Login.jsp?logintype=1'    # 显示最新消息的页面
DOCUMENT_URL = 'http://notes.stu.edu.cn/csweb/list.jsp'
WEBSITE_ENCODING = 'GBK'
NOTIFICATION_COUNT = 10

def get_most_updated(pageindex):
    # the result of urlencode is already str
    post_data = urllib.parse.urlencode({
        "pageindex": pageindex
        # not needed
        # "pagesize": NOTIFICATION_COUNT,
    })

    # before post the data, the data need to be the form of bytes
    post_data = post_data.encode(WEBSITE_ENCODING)
    # postData = urllib.urlencode(postDict)

    req = urllib.request.urlopen(DOCUMENT_URL, post_data)

    content = req.read().decode(WEBSITE_ENCODING)

    # maybe no count limitation
    return parse(content, count=NOTIFICATION_COUNT)

    # resp = urllib.request.urlopen(DOCUMENT_URL)
    # content = resp.read().decode(WEBSITE_ENCODING)
    # return parse(content, count=NOTIFICATION_COUNT)


if __name__ == "__main__":
    messages = get_most_updated()
    for msg in messages:
        print(msg.to_dict())