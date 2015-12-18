# coding=utf-8

from class_member.helper import getClassFromCredit, toJson

def get(class_id):
    content = getClassFromCredit.getClassByClassNo(class_id)
    if content is None:
        return None
    return toJson.to_json(content, class_id)

if __name__ == "__main__":
    data = get(80931)
    print(data)
