# coding=utf-8
import urllib
import urllib.request
from .oa_parser import parse

# CONSTANTS
UPDATED_ADDR = 'http://notes.stu.edu.cn/login/Login.jsp?logintype=1'    # 显示最新消息的页面
DOCUMENT_URL = 'http://office.stu.edu.cn/csweb/list.jsp'
WEBSITE_ENCODING = 'GBK'
NOTIFICATION_COUNT = 20

def get_most_updated(pageindex):

    postDict = urllib.parse.urlencode({
        "pageindex": pageindex,
        "pagesize": NOTIFICATION_COUNT,
    })

    postData = urllib.urlencode(postDict)

    req = urllib2.Request(DOCUMENT_URL, postData)

    content = resp.read().decode(WEBSITE_ENCODING)

    # maybe no count limitation
    return parse(content, count=NOTIFICATION_COUNT)

    # resp = urllib.request.urlopen(DOCUMENT_URL)
    # content = resp.read().decode(WEBSITE_ENCODING)
    # return parse(content, count=NOTIFICATION_COUNT)


if __name__ == "__main__":
    messages = get_most_updated()
    for msg in messages:
        print(msg.to_dict())