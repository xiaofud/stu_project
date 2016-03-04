# coding = utf-8
import os
import time
import json

NOTIFICATION_FILENAME = "notification.txt"
dirname = os.path.dirname(__file__)
if dirname == "":
    NOTIFICATION_FILE_PATH = "notifications" + str(os.path.sep) + NOTIFICATION_FILENAME
else:
    NOTIFICATION_FILE_PATH = dirname + str(os.path.sep) + "notifications" + str(os.path.sep) + NOTIFICATION_FILENAME

def backup_previous():
    if os.path.exists(NOTIFICATION_FILE_PATH):
        with open(NOTIFICATION_FILE_PATH) as f:
            obj = json.load(f)
            with open(NOTIFICATION_FILE_PATH + "_" + str(obj["timestamp"]), "w") as o:
                json.dump(obj, o)
                print("backup finished!")

def new_notification():
    backup_previous()
    count = input("input pictures count(default 3): ")
    assert isinstance(count, str)
    if count.strip() == "":
        count = int(3)
    else:
        count = int(count)

    notifications = []

    for i in range(1, count + 1):
        print("info for ", i)
        url = input("picture url: ")
        link = input("link to go to: ")
        description = input("description: ")

        notification = {
            "id": i,
            "url": url,
            "link": link,
            "description": description
        }
        notifications.append(notification)

    timestamp = int(time.time())

    return {
        "notifications": notifications,
        "timestamp": timestamp
    }


def get_notification():
    if os.path.exists(NOTIFICATION_FILE_PATH):
        with open(NOTIFICATION_FILE_PATH) as f:
            return json.load(f)
    return None


if __name__ == "__main__":
    print(NOTIFICATION_FILE_PATH)
    obj =  new_notification()
    with open(NOTIFICATION_FILE_PATH, "w") as f:
        json.dump(obj, f, ensure_ascii=False)
        print("生成成功!")


