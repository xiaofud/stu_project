# coding = utf-8
"""
    用于解析成绩信息
"""

REMOVAL_DATA = "<tr>	<th width='55'>开课班号</th>	<th>课程名称</th>	<th width='140'>任课教师</th>	<th width='40'>成绩</th>	<th width='30'>学分</th></tr>"

TEST_DATA = """
    <tr>	<td>71609</td>			<td>[ELC2]英语(ELC2)	</td><td>陈琳</td>		<td>86</td>			<td>4.0</td>	</tr>
    <tr>	<td>72295</td>			<td>[SOC6110A]马克思主义基本原理[SOC0610]</td>	<td>程英姿</td>	<td>85</td>		<td>3.0</td>	</tr>
<tr><td>72849</td><td>[CST1301A]程序设计基础[CST9104]</td><td>方若宇</td><td>94</td><td>4.0</td></tr><tr><td>72955</td><td>[ENC1101A]工程设计导论[ENC9105]</td><td>包能胜/吴保昭(实验)</td><td>86</td><td>2.0</td></tr><tr><td>72973</td><td>[ENC1102A]化学导论[ENC9110]</td><td>尹业高</td><td>85</td><td>1.0</td></tr><tr><td>72976</td><td>[ENC1103A]生物学导论[ENC9120]</td><td>游翠红</td><td>86</td><td>1.0</td></tr><tr><td>73071</td><td>[CST1307A]线性代数[CST9105]</td><td>廖海泳                                                      </td><td>92</td><td>2.0</td></tr><tr><td>73073</td><td>[CST1501A]计算科学导论[CST9106]</td><td>蔡玲如                                                      </td><td>89</td><td>2.0</td></tr><tr><td>72857</td><td>[CIS6031A]汕大整合思维[CIS2031]</td><td>Wai-man Kwok/李洪利/孙金峰/王雨函</td><td>90</td><td>2.0</td></tr><tr><td>71690</td><td>[MAT1801A]微积分B-I</td><td>王仙桃                                                      </td><td>90</td><td>4.0</td></tr><tr><td colspan='5'><b>共选修课程10门25.0个学分，实际获得25.0个学分</b></td></tr></table>
"""



from html.parser import HTMLParser

class Grade(object):

    def __init__(self, class_num, class_name, class_teacher, class_grade, class_credit):
        self.class_num = class_num
        self.class_name = class_name
        self.class_teacher = class_teacher
        self.class_grade = class_grade
        self.class_credit = class_credit

    def to_dict(self):
        return {
            "class_number": self.class_num,
            "class_name": self.class_name,
            "class_teacher": self.class_teacher,
            "class_grade": self.class_grade,
            "class_credit": self.class_credit
        }

    def __repr__(self):
        return repr(self.to_dict())

class GradeParser(HTMLParser):
    """
        用于解析成绩
    """

    def __init__(self):
        
        super(GradeParser, self).__init__()

        
        # 标记解析是否已经完成
        self.finished = False

        # 计数器，用于判断当前的属性是哪一项内容
        self.point = 0

        # 存储Grade数据
        self.data = list()

        self.class_num = None
        self.class_name = None
        self.class_teacher = None
        self.class_grade = None
        self.class_credit = None

    def clear(self):
        """
            重置整个parser的状态
        :return:    None
        """
        self.data = list()  # 之前的数据已经返回出去了

        self.class_num = None
        self.class_name = None
        self.class_teacher = None
        self.class_grade = None
        self.class_credit = None

    def get_grades(self, raw_data):
        """
            封装了对feed的调用，会在完成后重置整个parser的状态
        :return:
        """
        self.feed(raw_data)
        grades = self.data
        self.clear()
        return grades


    def handle_starttag(self, tag, attrs):
        # print(tag)
        super(GradeParser, self).handle_starttag(tag, attrs)

    def handle_data(self, data):
        assert isinstance(data, str)
        # 已经去除了数据的空白
        data = data.strip()
        if data.__contains__("共"):
            self.finished = True

        # 解析没有完成，而且数据不是空白的话
        if not self.finished and data != "":
            if self.point == 0:
                # 开课班号
                self.class_num = data
            elif self.point == 1:
                self.class_name = data
            elif self.point == 2:
                self.class_teacher = data
            elif self.point == 3:
                self.class_grade = data
            elif self.point == 4:
                self.class_credit = data
                self.data.append(Grade(self.class_num, self.class_name, self.class_teacher, self.class_grade, self.class_credit))

            # 变化point的指向
            if self.point == 4:
                # 从头开始
                self.point = 0
            else:
                self.point += 1



if __name__ == "__main__":
    parser = GradeParser()
    print(parser.get_grades(TEST_DATA))



