#! /usr/bin/env python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/pi/Desktop/STU_Project/")

from server import app as application
application.secret_key = 'nothing secret'

