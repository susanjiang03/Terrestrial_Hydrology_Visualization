import sys
import csv
import os
import numpy as np
import json
#from pprint import pprint

# this function return a dictionay, key is index, value is corresponding [lat,lon]
# scan datafile indicators.csv
# eg {0: [lat0, lon0], 1: [lat1,lon1]}
in_filename = "1980-03-01.csv"
json_fileName = 'dict_index_lat_lon.json'
def write_locatoins_dict_to_json(json_fileName ):
	locationDict = {}
	with open(in_filename, 'rb') as in_f:
		reader = csv.reader(in_f)
		next(reader, None) 
		for line in reader:
			index,lat,lon = int(line[0]),line[2],line[3]
			if index not in locationDict.keys():
				locationDict[index] = [lat, lon]
				print index, locationDict[index]
			else:
				print str(index) + " already in dict kyes"
	in_f.close()
	print len(locationDict)

	#print locationDict
	with open(json_fileName, 'w') as fp:
	     json.dump(locationDict, fp)
	fp.close()




    