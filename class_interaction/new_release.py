# coding = utf-8
"""
    用于生成新的版本信息, 同时备份老版本的发布信息
"""

import json
import time
import os
# 一些常量
DOWNLOAD_ADDRESS = "http://10.28.31.32/share/syllabus.apk"

# 存储文件名
VERSION_FILE = "version.txt"

'''
{
    "versionCode": 7,
    "versionName": "ver 1.4",
    "versionReleaser": "smallfly",
    "download_address": "http://10.22.27.65/share/syllabus.apk",
    "apk_file_name": "syllabus_v1.3.apk",
    "versionDate":1445613278,
    "description": "修改主界面UI, 增加删除吹水功能。\nIOS COMING SOON!\n如果自动更新失败需要卸载之前版本\n自动下载好的新版本在sd卡的download目录下"
}
'''

def backup_previous_release():
    """
    备份上一次的version文件
    :return:
    """
    if not os.path.exists(VERSION_FILE):
        print("没有之前的发布信息")
        return
    with open(VERSION_FILE) as f:
        version_json = json.load(f)
        filename = "version_" + str(version_json["versionCode"]) + ".txt"
        with open(filename, "w") as f:
            json.dump(version_json, f)
            print("成功备份: " + filename)

def input_update_description():
    description = str()
    line = input("输入描述信息(空行为结束): \n")
    while line.strip() != "":
        description += line + "\n"
        line = input()

    return description.strip()


def update_release_note():
    """
    读取这次发布的信息
    :return: JSON
    """
    note = {
        "versionCode": "版本号",
        "versionName": "版本名称",
        "versionReleaser": "发布者",
        "apk_file_name": "apk文件名",
        # "description": "版本描述信息"
    }

    for key in note:
        # 输出提示信息同时改变键值
        note[key] = input(note[key] + ":\n")

    note["description"] = input_update_description()

    # 添加一些其他信息
    note["versionDate"] = int(time.time())
    note["download_address"] = DOWNLOAD_ADDRESS

    #return json.dumps(note)
    with open(VERSION_FILE, "w") as f:
        json.dump(note, f)
        print("生成了新的版本文件!")

if __name__ == "__main__":
    backup_previous_release()
    update_release_note()
    # print(input_update_description())