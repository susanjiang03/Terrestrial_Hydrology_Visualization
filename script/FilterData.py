import csv
import os
import errno
import numpy as np
import json
import math
import datetime
from GetData import *
import matplotlib.pyplot as plt

CURRENT_DIR = os.getcwd()
raw_dataFile = "indicators.csv"
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResult_DIR = PARENT_DIR + "/MeanShiftResult"
MeanShiftResult_IMAGES_DIR = MeanShiftResult_DIR+ "/IMAGES"
MeanShiftResult_LABELCSV_DIR = MeanShiftResult_DIR+ "/LABELCSV"
MeanShiftResult_CLUSTERCENTERSCSV_DIR = MeanShiftResult_DIR+ "/ClusterCentersCSV"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"
GRID_INDEXLIST_JSON = "grid_indexList.json"
INDEX_LATLON_JSON = "index_LatLon.json"
DATE_LIST_TXT = "date_list.txt"

HEADER = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']


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
@column name in header
@value : filter by the value
@return_column_index : return the index 
return a list of row with the index
exclude header
'''
def filter_by_columnName_value(in_fileName, column_name, value, return_column_name):
    #if index not in locationlist
	data_as_list = []
	with open(in_fileName, 'rb') as in_f:
		datareader = csv.reader(in_f)
		header = datareader.next()
		index = header.index(column_name)
		return_column_index = header.index(return_column_name)
		next(datareader, None)
		print "\nStart filtering data for index %d in file: \n%s"%(index,in_fileName)
		for line in datareader:
			if int(line[index]) == value:
				return_column = line[return_column_index]
				data_as_list.append(return_column)
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
	in_fileName = '%s/P%r_N%d/P0.1_N1_1991-12-01.csv'%(SampleCSV_DIR, percentage, sampleNum)
	# print len(filter_by_index_value(in_fileName,4, 1))
	# print len(filter_by_index_value(in_fileName,4, 2))
	# print len(filter_by_index_value(in_fileName,4, 3))
	for c in range(0,7):
		for i in range(4,38):
			plt.figure(1)
			plt.clf()
			data_as_list = filter_by_columnName_value(in_fileName,'[ALL]_Q0.1', c, HEADER[i])
			plot_data = map(int,data_as_list[:])
			plt.hist(plot_data, bins= range(0,95,5))
			#(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
			imageName = '/%s/HISTOGRAMS/P0.1_N1_Q0.1_[ALL]/C%r_V%d_%s.jpg'%(MeanShiftResult_DIR,c,i, HEADER[i])
			dest = imageName[:imageName.rfind("/")]
			try:
				os.makedirs(dest)
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
				else:
					pass
			plt.savefig(imageName)
			plt.clf()
			print "save %s"%imageName
	





    


