# coding=utf-8
import urllib
import urllib.request
# import html
from .oa_parser import parse

# CONSTANTS
UPDATED_ADDRESS = 'http://notes.stu.edu.cn/login/Login.jsp?logintype=1'    # 显示最新消息的页面
DOCUMENT_URL = 'http://notes.stu.edu.cn/csweb/list.jsp'
WEBSITE_ENCODING = 'GBK'
NOTIFICATION_COUNT = 20

def get_most_updated_oa_list(pageindex):
    # the result of urlencode is already str
    post_data = urllib.parse.urlencode({
        "pageindex": pageindex,
        # control the numbers
        "pagesize": NOTIFICATION_COUNT
    })

    # before post the data, the data need to be the form of bytes
    post_data = post_data.encode(WEBSITE_ENCODING)
    # postData = urllib.urlencode(postDict)

    resp = urllib.request.urlopen(DOCUMENT_URL, post_data)

    content = resp.read().decode(WEBSITE_ENCODING)

    # maybe no count limitation, yep
    return parse(content, count=NOTIFICATION_COUNT)

    # resp = urllib.request.urlopen(DOCUMENT_URL)
    # content = resp.read().decode(WEBSITE_ENCODING)
    # return parse(content, count=NOTIFICATION_COUNT)

def send_out_oa_page(url):
    try:
        resp = urllib.request.urlopen(url, timeout=7)
        # return html.unescape(resp.read().decode(WEBSITE_ENCODING))
        TEST_FILE_NAME = "output_html.html"
        content = resp.read().decode(WEBSITE_ENCODING)
        assert isinstance(content, str)
        str_need_to_replace = "<STYLE TYPE=\"text/css\">"
        str_need_to_add_on_the_front = "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">"
        content = content.replace(str_need_to_replace, str_need_to_add_on_the_front + "\n" + str_need_to_replace)
        # with open(TEST_FILE_NAME, "w") as f:
        #     f.write(content)
        return True, content
    except Exception as err:
        return False, None

if __name__ == "__main__":
    messages = get_most_updated_oa_list()
    for msg in messages:
        print(msg.to_dict())