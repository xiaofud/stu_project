# coding = utf-8
"""
解析考试的原始信息
"""

from html.parser import HTMLParser

"""
			<th scope="col">考试班号</th><th scope="col">课程名称</th><th scope="col">考试地点</th><th scope="col">考位号</th><th scope="col">主考</th><th scope="col">监考</th><th scope="col">时间</th><th scope="col">考生数</th><th scope="col">备注</th>
		</tr><tr class="DGItemStyle">
"""

TEST_DATA = """
<tr class="DGHeaderStyle">
			<td><a href="ExamDetail.aspx?ExamID=12349&amp;HighLight=" target="_blank">12349</a></td><td>[CST1501A]计算科学导论[CST9106]</td><td>讲堂四</td><td>61</td><td>蔡玲如</td><td>张凯东                                                      </td><td>第17周星期一第2场(2015.01.12  10:30-12:30)</td><td>69</td><td>&nbsp;</td>
		</tr><tr class="DGAlternatingItemStyle">
			<td><a href="ExamDetail.aspx?ExamID=11888&amp;HighLight=" target="_blank">11888</a></td><td>[ELC2]英语(ELC2)</td><td>E408</td><td>36</td><td>陈琳</td><td>David Roger Williams                                        </td><td>第17周星期一第3场(2015.01.12  13:30-15:30)</td><td>49</td><td>&nbsp;</td>
		</tr><tr class="DGItemStyle">
			<td><a href="ExamDetail.aspx?ExamID=12005&amp;HighLight=" target="_blank">12005</a></td><td>[MAT1801A]微积分B-I</td><td>E303</td><td>15</td><td>王仙桃</td><td>李芬兰/林福荣                                               </td><td>第17周星期三第2场(2015.01.14  10:30-12:30)</td><td>70</td><td>&nbsp;</td>
		</tr><tr class="DGAlternatingItemStyle">
			<td><a href="ExamDetail.aspx?ExamID=12350&amp;HighLight=" target="_blank">12350</a></td><td>[CST1307A]线性代数[CST9105]</td><td>讲堂四</td><td>69</td><td>廖海泳</td><td>蔡浩                                                        </td><td>第17周星期四第1场(2015.01.15  08:00-10:00)</td><td>74</td><td>&nbsp;</td>
		</tr><tr class="DGItemStyle">
			<td><a href="ExamDetail.aspx?ExamID=11962&amp;HighLight=" target="_blank">11962</a></td><td>[SOC6110A]马克思主义基本原理[SOC0610]</td><td>E301</td><td>15</td><td>贺明生</td><td>宋健/甄美玲                                                 </td><td>第18周星期一第2场(2015.01.19  10:30-12:30)</td><td>60</td><td>开卷</td>
		</tr><tr class="DGAlternatingItemStyle">
			<td><a href="ExamDetail.aspx?ExamID=12348&amp;HighLight=" target="_blank">12348</a></td><td>[CST1301A]程序设计基础[CST9104]</td><td>E303</td><td>36</td><td>于津</td><td>方若宇                                                      </td><td>第18周星期三第4场(2015.01.21  16:00-18:00)</td><td>68</td><td>&nbsp;</td>
		</tr>
	</table>

"""

# 考试班号	课程名称	考试地点	考位号	主考	监考	时间	考生数	备注

class Exam(object):

    def __init__(self, exam_class_number, exam_class, exam_location, exam_stu_position, exam_main_teacher, exam_invigilator, exam_time,
                 exam_stu_numbers, exam_comment):
        self.exam_class_number = exam_class_number
        self.exam_class = exam_class
        self.exam_location = exam_location
        self.exam_stu_position = exam_stu_position
        self.exam_main_teacher = exam_main_teacher
        self.exam_invigilator = exam_invigilator
        self.exam_time = exam_time
        self.exam_stu_numbers = exam_stu_numbers
        self.exam_comment = exam_comment

    def to_dict(self):
        return {
            "exam_class": self.exam_class,
            "exam_location": self.exam_location,
            "exam_stu_numbers": self.exam_stu_numbers,
            "exam_main_teacher": self.exam_main_teacher,
            "exam_stu_position": self.exam_stu_position,
            "exam_comment": self.exam_comment,
            "exam_time": self.exam_time,
            "exam_class_number": self.exam_class_number,
            "exam_invigilator": self.exam_invigilator
        }

    def __repr__(self):
        return repr(self.to_dict())

class ExamParser(HTMLParser):

    properties = ['exam_class_number', ' exam_class', ' exam_location', ' exam_stu_position', ' exam_main_teacher', ' exam_invigilator', ' exam_time', 'exam_stu_numbers', ' exam_comment']

    def __init__(self):
        super(ExamParser, self).__init__()
        self.finished = False
        # self.exam_count = exam_count
        self.exam_list = list()
        self.point = 0

        # 存储数据的变量
        self.exam_class_number = None
        self.exam_class = None
        self.exam_location = None
        self.exam_stu_position = None
        self.exam_main_teacher = None
        self.exam_invigilator = None
        self.exam_time = None
        self.exam_stu_numbers = None
        self.exam_comment = None

    def handle_data(self, data):
        assert isinstance(data, str)
        data = data.strip()
        # 注意最后一项是备注，多半可能是空
        if data == "" and self.point != len(ExamParser.properties) - 1:
            return
        # print(data)
        # x.y = z
        setattr(self, ExamParser.properties[self.point], data)
        self.point += 1

        if self.point == len(ExamParser.properties):
            # make a new Exam object
            arguments = list()
            for name in ExamParser.properties:
                arguments.append(getattr(self, name))
            exam = Exam(*arguments)
            self.exam_list.append(exam)

            self.point = 0



# def code_generator(input_str):
#     assert isinstance(input_str, str)
#     elements = input_str.split(",")
#     dict_data = dict()
#     for element in elements:
#         dict_data[element.strip()] = "self." + element.strip()
#     for element in dict_data:
#         print("\"" + element + "\"", ": ", dict_data[element], ",", sep="")


if __name__ == "__main__":
    # code_generator("exam_class_number, exam_class, exam_location, exam_stu_position, exam_main_teacher, exam_invigilator, exam_time, exam_stu_numbers, exam_comment")
    # print("exam_class_number, exam_class, exam_location, exam_stu_position, exam_main_teacher, exam_invigilator, exam_time,exam_stu_numbers, exam_comment".split(","))
    parser = ExamParser()
    parser.feed(TEST_DATA)
    for exam in parser.exam_list:
        print(exam.exam_time)
