import csv
import os
import errno
import numpy as np
import json
import math
import datetime
from GetData import *

CURRENT_DIR = os.getcwd()
raw_dataFile = "indicators.csv"
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResult_DIR = PARENT_DIR + "/MeanShiftResult"
MeanShiftResult_IMAGES_DIR = MeanShiftResult_DIR+ "/IMAGES"
MeanShiftResult_LABELCSV_DIR = MeanShiftResult_DIR+ "/LABELCSV"
MeanShiftResult_CLUSTERCENTERS_DIR = MeanShiftResult_DIR+ "/ClusterCenters"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"
GRID_INDEXLIST_JSON = "grid_indexList.json"
INDEX_LATLON_JSON = "index_LatLon.json"
DATE_LIST_TXT = "date_list.txt"


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
		#print "\nStart filtering data for row[%d] = %s in file: \n%s"%(index,str(value), in_fileName)
		for line in datareader:
			if str(line[index]) == str(value):
				data_as_list.append(line)
		#print "Finished"
	in_f.close()
	return data_as_list


if __name__ == "__main__":
		#print 'from filterData.py'
	percentage = 0.1
	sampleNum = 1
	quantile = 0.1
	string_list_of_index = '[ALL]'
	column_name = 'P%r_N%d_Q%r'%(percentage,sampleNum,quantile)
	date = '1991-12-01'
	#in_fileName = '%s/LABELCSV/P%r_N%d/labelsClusters_P%r_N%d_%s.csv'%(MeanShiftResult_DIR,percentage,sampleNum, percentage,sampleNum, date)
	in_fileName = '%s/P%r_N%d/labelClusters_P0.1_N1_1991-12-01.csv'%(MeanShiftResult_LABELCSV_DIR, percentage, sampleNum)
	# print len(filter_by_index_value(in_fileName,4, 1))
	# print len(filter_by_index_value(in_fileName,4, 2))
	# print len(filter_by_index_value(in_fileName,4, 3))
	for each in filter_by_index_value(in_fileName,4,3):
		print each[0]




    


