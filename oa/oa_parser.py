# coding=utf-8

import html.parser

PAGE_ADDR = 'http://notes.stu.edu.cn'

class OAObject(object):
    def __init__(self, title, url, department, date):
        self.title = title
        self.url = url
        self.department = department
        self.date = date

    def __str__(self):
        return "[" + self.title + "]" + "(" + self.department + ") " + self.date + "\t" + self.url

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'department': self.department,
            'date': self.date
        }

class OAParser(html.parser.HTMLParser):

    def error(self, message):
        pass

    finished = False
    start_handle_data = False
    to_handle_data = 0  # 用于判断什么时候去获取发布单位和日期
    handled_tag_a = False
    objects = []
    _count = 0

    title = None
    url = None
    department = None
    date = None

    def __init__(self, count):
        """
        :param count:   每页的通知数
        :return:
        """
        super().__init__()
        self.count = count

    def handle_starttag(self, tag, attrs):
        # attrs 是 [('href', 'http://xxx')]
        if tag == 'tr':  # lower_case
            tmp = dict(attrs)
            cls = tmp.get('class', None)
            if cls is not None and cls == 'datalight' and not self.finished:
                # print(tmp)
                self.start_handle_data = True

        if self.start_handle_data:
            if tag == 'a':
                self.handled_tag_a = False
                attrs = dict(attrs)
                self.title = attrs['title']
                self.url = PAGE_ADDR  + attrs['href']

    def handle_data(self, data):
        if self.start_handle_data:
            data = data.strip()
            if data == "":
                return  # just pass
            if self.to_handle_data == 1:    # 处理的是发布单位
                self.to_handle_data += 1
                self.department = data
            elif self.to_handle_data == 2:
                self.date = data
                self.to_handle_data = 0
                # 一条通知信息已经读取完毕
                # print(self.date, self.department)
                obj = OAObject(self.title, self.url, self.department, self.date)
                self.objects.append(obj.to_dict())
                self._count += 1



    def handle_endtag(self, tag):
        if self.start_handle_data and tag == 'a':
            self.to_handle_data = 1

        if tag == 'tbody':
            self.start_handle_data = False
            self.finished = True

def parse(content, count):
    parser = OAParser(count)
    parser.feed(content)
    return parser.objects

