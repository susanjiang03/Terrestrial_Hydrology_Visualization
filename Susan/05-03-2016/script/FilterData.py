import csv
import os
import errno
import numpy as np
import json
import math
import datetime
import GetData

CURRENT_DIR = os.getcwd()
raw_dataFile = "indicators.csv"
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResutl_DIR = PARENT_DIR + "MeanShiftResutl"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"
GRID_INDEXLIST_JSON = "grid_index.json"
INDEX_LATLON_JSON = "index_LatLon.json"


'''
read in_fileName, filter by date, write csv file 
@in_fileName
@date: a string of date in the dateList , e.g. "1990-12-01"
return a list, including header
'''
def filter_by_date(in_fileName, date):
	data_as_list = []
	if is_in_dateList(date):
		with open(in_fileName, 'rb') as in_f:
			datareader = csv.reader(in_f)
			next(datareader, None)
			print "\nStart filtering data for date :"+date
			for line in datareader:
				if line[1] == date:
					data_as_list.append(line)
			print "Finished"
		in_f.close()
	else: 
		print "Error.Invalid date."+ date
	return data_as_list

'''
read in_fileName, filter by index, 
@in_fileName
@index: location index 
return a list of row with the index
exclude header
'''
def filter_by_index(in_fileName, index):
    #if index not in locationlist
	data_as_list = []
	with open(in_fileName, 'rb') as in_f:
		datareader = csv.reader(in_f)
		next(datareader, None)
		print "\nStart filtering data for index %d in file: \n%s"%(index,in_fileName)
		for line in datareader:
			if int(line[0]) == index:
				data_as_list.append(line)
		#print "Finished"
	in_f.close()
	return data_as_list
	# else: 


'''
read in_fileName, filter by index, 
@in_fileName: csv file
@index: index of column in the file
@value : filter by the value
return a list of row with the index
exclude header
'''
def filter_by_index_value(in_fileName, index, value):
    #if index not in locationlist
	data_as_list = []
	with open(in_fileName, 'rb') as in_f:
		datareader = csv.reader(in_f)
		next(datareader, None)
		print "\nStart filtering data for row[%d] = %s in file: \n%s"%(index,str(value), in_fileName)
		for line in datareader:
			if int(line[index]) == value:
				data_as_list.append(line)
		#print "Finished"
	in_f.close()
	return data_as_list


if __name__ == "__main__":
	print 'from filterData.py'
