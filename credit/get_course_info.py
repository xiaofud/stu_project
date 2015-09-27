# -*- coding: utf-8 -*-
from html.parser import HTMLParser
TESTDATA ="""<td><a id="DataGrid1_ctl05_HyperLink1" href="../Info/DisplayKkb.aspx?ClassID=81229&amp;auth=82EEDB110657D1EE375CAF4F6652270E" target="_blank">81229</a>
									</td><td><a href="../Course/DispCourseInfo.aspx?id=4644" target="_blank">[EEG2053A]电工电子学</a></td><td>4.0</td><td><a href="../Teacher/ClassTeacherInfo.aspx?ClassID=81229" target="_blank">柳平/张琼/陈征(实验)/夏隽娟(实验)                                               </a></td><td><a href="../CoursePlan/viewclassroom.aspx?ClassID=81229" target="_blank">D座504                                                                          </a></td><td>1 -14     </td><td>               </td><td>67             </td><td>               </td><td>               </td><td>67             </td><td>               </td><td>               </td>
"""

# TESTDATA="""Not tag content<td>包含了a标签在td里面<a>link</a></td>
# """

# 对于每一节课来说一共有13个td标签
# <td>班号</td><td>课程名称</td><td>学分数</td><td>教师</td><td>课室</td><td>起止周</td><td>周日</td><td>周一</td><td>周二</td><td>周三</td><td>周四</td><td>周五</td><td>周六</td>


def fill_empty_tag(content, tag, value=-1):
    assert isinstance(content, str)
    search = '<' + tag +'></' + tag + '>'
    replace = '<' + tag +'>' + str(value) + '</' + tag + '>'
    return content.replace(search, replace)

def get_class_html_parts(content):
    start_str = '<tr class="DGItemStyle"'
    end_str = '<tr class="DGFooterStyle">'
    start_index = content.find(start_str)
    end_index = content.find(end_str)
    content = content[start_index: end_index]
    # print(content)
    # print(content)
    # 把下面改成迭代即可

    class_strs = []

    # 开始找第一个a
    a_index = content.find('<a')   # 要把原始的格式转化为可读的形式
    tr_index = content.find('</tr>')

    while a_index != -1:  # 说明还有课
        class_str = content[a_index: tr_index]
        class_str = "<td>" + class_str
        class_strs.append(class_str)

        # 重新设置content
        content = content[tr_index + len('</tr>'):]     # 跳过这节课
        a_index = content.find('<a')   # 要把原始的格式转化为可读的形式
        tr_index = content.find('</tr>')

    return class_strs


class Lesson(object):
    """课程类"""

    def __init__(self, cls_num=0, cls_name=str(), cls_credit=0, cls_teacher=str(), cls_room=str(), cls_duration=str(), cls_schedule={}):
        self.num = cls_num
        self.name = cls_name
        self.credit = cls_credit
        self.teacher = cls_teacher
        self.room = cls_room
        self.duration = cls_duration
        self.schedule = cls_schedule

    def __str__(self):
        # cls_str = 'class name: ' + self.name + '\n' + 'class number: ' + self.num + '\n' + 'class credit:' + str(self.credit) +'\n' + 'teacher: ' + self.teacher\
        # + '\n' + 'classroom: ' + self.room + '\n'
        # for day in self.schedule:
        #     if self.schedule[day] != "":
        #         cls_str += str(day) + " : " + self.schedule[day]
        cls_str = 'class name: ' + self.name + '\n' + 'teacher: '  + self.teacher + '\n' + 'class number: ' + str(self.num) + '\n' + 'class room: ' + self.room + "\n"\
                + 'duration: ' + self.duration + '\n'
        for day in self.schedule:
            if self.schedule[day].strip() != '':
                cls_str += '周' + str(day) + ': ' +  self.schedule[day] + '\n'
        return cls_str

    @staticmethod
    def add_quotes(mystr, quote="\""):
        return quote + mystr + quote

    @staticmethod
    def jsonfy_all(classes):
        json_data = "{" + Lesson.add_quotes("classes") + ":["
        for cls in classes:
            json_data += cls.to_json() + ","
        json_data = json_data[: -1] + "]}"   # 去除末尾的逗号以及添加大括号
        return json_data

    def to_json(self):
        days = []
        for day in self.schedule:
            if self.schedule[day].strip() != '':
                cls_str = self.add_quotes( "w" + str(day)) + ":" + self.add_quotes(self.schedule[day])  # eg. "w2":"AB"
            else:
                cls_str = self.add_quotes( "w" + str(day)) + ":" + self.add_quotes("None")  # eg. "w3":"None"
            days.append(cls_str)

        days_str = "{"
        for day in days:
            days_str += day + ","
        days_str = days_str[: -1]  + "}" # 去掉末尾的","

        json_data =  "{" + self.add_quotes("name") + ":" + self.add_quotes(self.name) + ',' \
                + self.add_quotes("id") + ":" + self.add_quotes(self.num) + "," \
                + self.add_quotes("teacher") + ":" + self.add_quotes(self.teacher) + "," \
                + self.add_quotes("room") + ":" + self.add_quotes(self.room) + "," \
                + self.add_quotes("duration") + ":" + self.add_quotes(self.duration) + "," \
                + self.add_quotes("days") + ":"  + days_str   \
                + "}"
        return json_data






class ClassParser(HTMLParser):  # 空标签会被跳过

    def __init__(self):
        super().__init__()
        self.inside_td = False
        self.cur_tag = ''
        self.count = -1
        self.data = []
        self.lesson = None

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.inside_td = True
        self.cur_tag = tag  # 记录当前tag

    def handle_endtag(self, tag):
        self.cur_tag = ''   # 说明离开了当前的标签


    def handle_data(self, data):    # 默认的话，没有处在标签内的data也会被这里处理
        if self.cur_tag != "":  # 去掉不在标签里面的内容
            self.count += 1
            self.data.append(data.strip())
            # print(self.count, '当前的data属于', self.cur_tag, '标签:', data.strip())
            if self.count == 12:
                lessons = self.data[6:]    # 第六个数据开始为上课的天数
                # print(len(lessons))
                schedule = {}
                for i in range(7):
                    schedule[i] = lessons[i]    # 周几的第几节课
                self.data = self.data[:6]   # 删除后面的记录
                self.data.append(schedule)
                lesson = Lesson(*self.data)
                # print(lesson)
                self.lesson = lesson

    # def close(self):
        # self.clear()
        # super().close()


    def clear(self):
        # print("cleared")
        self.inside_td = False
        self.cur_tag = ''
        self.count = -1
        self.data = []


class Parser(HTMLParser):

    count = 0

    def handle_starttag(self, tag, attrs):
        print('start',tag)

    def handle_endtag(self, tag):
        print('end',tag)

    def handle_data(self, data):
        self.count += 1
        print(self.count, data)



if __name__ == "__main__":
    content = ''
    with open('result_page', 'r') as f:
        content = f.read()
    content = get_class_html_parts(content)
    parser = ClassParser()
    for lesson in content:
        parser.feed(lesson)
        parser.close()