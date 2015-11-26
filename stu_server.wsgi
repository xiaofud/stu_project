import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/pi/Desktop/stu_project/")

from server import app as application
application.secret_key = 'nothing secret'

