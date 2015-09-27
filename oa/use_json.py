# coding=utf-8
import json
# from io import StringIO
import urllib.request

# obj = json.dumps(['foo', {'bar': ('bar', None, 1.0, 2)}])
# io = StringIO()
#
# nwad = {'name': 'nwad', 'age': 19, 'school': 'STU'}
#
# json.dump(nwad, io, indent=4)
# print(io.getvalue())


# parse json

HOST_ADDR = 'http://127.0.0.1:5000/oa'
resp = urllib.request.urlopen(HOST_ADDR)
json_data = resp.read().decode('utf-8')
print(json.loads(json_data))