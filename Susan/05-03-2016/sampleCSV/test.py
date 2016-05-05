import json
from pprint import pprint

d = {}
with open("indexLocation_dict.json") as json_data:
	d = json.load(json_data)
print d['97278']
print d
