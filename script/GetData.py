import csv
import os
import errno
import numpy as np
import json
import math
import ast
from pprint import pprint
from numpy import loadtxt

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
read date_list.txt in CURRENT_DIR
dataList.txt must exist in the directroy
call  after run populate_date_csv_files()
return a list of date
'''
def get_date_list():
   fo = open(DATE_LIST_TXT)
   string_date_list = fo.readline()
   date_list = string_date_list.strip().split(" ")
   date_list.sort()
   #print date_list
   return date_list

'''
check if the date in date_list
'''
def validate_ate(date):
	date_list = get_date_list()
	if date not in date_list:
	   print "Error. %snot in list"%s
	   return 

'''
read from *_sample_*.txt file, return a list of integer
run after sample txt file generated
@in_file : smapel txt file name 
rertun a list of sample locations
'''
def get_sample_locations_list(percentage,sampleNum):

	sample_fileName = SampleLocationsTXT_DIR + "/P%r/P%r_N%d.txt"%(percentage,percentage,sampleNum)
	fo = open(sample_fileName)
	r = fo.readline()
	string_indexList = r.strip().split(" ")
	sample_indexList = map(int, string_indexList)
	#print sample_indexList
	return sample_indexList


''' get header of the in_fileName,'''
def get_header(in_fileName):
	header = []
	with open(in_fileName, 'rU') as in_f:
		reader = csv.reader(in_f)
		data_as_list = list(reader)
		header = data_as_list[0]
	in_f.close()
	return header


'''
# #after populated index_LatLon.json file , by populate_index_LatLon_json()
# #return a list of ['lat','lon'], where key in index 
# '''
# def get_location_lat_lon_by_index(locationIndex):
# 	dict_index_LatLon = {}
# 	with open(INDEX_LATLON_JSON) as data_file:    
# 	    data = json.load(data_file)
# 	#pprint(data)
# 	dict_index_LatLon = map(float,data)
# 	print dict_index_LatLon
# 	print type(dict_index_LatLon)
# 	list_lat_lon = dict_index_LatLon[float(locationIndex)]
# 	print list_lat_lon

'''
in_filename : dir + fileName  (/*/*.csv)
return datamatrix need by a list of column index in the csv file  
Assume
'''

def get_data_as_list(in_fileName, list_of_index):
	
	in_data_as_list = []
	with open(in_fileName, 'rU') as in_f:
		reader = csv.reader(in_f)
		data_as_list = list(reader)
	in_f.close()
	out_data_as_list = []
	for row in data_as_list[1:]:
		newRow = []
		for i in list_of_index:
			value = row[i]
			#if is digit
			if value.isdigit():
				newRow.append(ast.literal_eval(value))  #data of the variable
			else:  #string
				newRow.append(value )
		out_data_as_list.append(newRow)
	return out_data_as_list






