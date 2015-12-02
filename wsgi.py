import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/smallfly/programming_projects/python/stu_project/")

from server import app as application
application.secret_key = 'sodijfoisajdfiojsdoiafjmn'
if __name__ == "__main__":
	application.run(host="0.0.0.0")
