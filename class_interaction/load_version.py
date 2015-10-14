# coding = utf-8
import os
import json


base_dir = os.path.dirname(__file__)
VERSION_FILE = "version.txt"
filename = os.path.join(base_dir, VERSION_FILE)

def load_version():
    if os.path.exists(filename):
        with open(filename, encoding="utf-8") as f:
            json_obj = json.loads(f.read())
        return json_obj
    return None

if __name__ == "__main__":
    version =  load_version()
    print(version['description'], version['download_address'])

