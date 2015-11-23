# coding = utf-8
"""
添加一节公共课程用于全球吹水
"""
from .database_models import *

# def __init__(self, number, name, credit, teacher, room, span, time_, start_year, end_year, semester):

PUBLIC_CLASS_ARGUMENTS = ["0", "public_class", "0.0", "None", "None", "None", "None", "0", "0", "0"]

def add_public_class():
    pub_class = ClassModel(*PUBLIC_CLASS_ARGUMENTS)
    rev_val = insert_to_database(pub_class)
    if rev_val[0]:
        print("成功添加公共课程")
        return True, None
    else:
        return rev_val

