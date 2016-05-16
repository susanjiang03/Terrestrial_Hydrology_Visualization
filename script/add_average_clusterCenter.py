import math
import os
import errno
import csv
import datetime
import json
from random import shuffle
from FilterData import *
from  GetData import *
from PopulateFiles import *


CURRENT_DIR = os.getcwd()
raw_dataFile = "indicators.csv"
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResult_DIR = PARENT_DIR + "/MeanShiftResult"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"
GRID_INDEXLIST_JSON = "grid_indexList.json"
INDEX_LATLON_JSON = "index_LatLon.json"
DATE_LIST_TXT = "date_list.txt"
LIST_OF_ALL_DATA = get_date_list() 
HEADER = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']

def add_average_to_cluterCenter_csv(in_fileName):

    date_list = get_date_list()
    new_date_list = date_list[ date_list.index('1991-12-01') : ]
    header = get_header(in_fileName)
    data_as_list = get_data_as_list(in_fileName, range(0,len(header)))
    #print data_as_list
    out_data_list = []
    header.extend(['average'])
    out_data_list.append(header)
    for date in new_date_list[:]:
    	list_of_ave_center = []
    	filter_data_as_list = [row for row in data_as_list if row[1] == date ]
    	#print filter_data_as_list
    	for row in filter_data_as_list:
    		#print row
    		ave = reduce(lambda x, y: float(x) + float(y), row[4:]) / len(row[4:])
    		#print ave
    		list_of_ave_center.append(ave)
    		row.append(ave)
    	list_of_ave_center.sort()
    	out_data_list.extend(filter_data_as_list)
    populate_data_as_list_to_csv_file(out_data_list,in_fileName)


def write_times_to_clusterCenter_csv(in_fileName):
	out_data_list =[]
	header = get_header(in_fileName)
	data_as_list = get_data_as_list(in_fileName,range(0,len(header)))
	header.append('times')
	out_data_list.append(header)
	list_of_ave =[ float(row[-1]) for row in data_as_list]
	# print list_of_ave
	min_ave = min(list_of_ave)
	# print min_ave
	times = [ a/min_ave for a in list_of_ave]
	# print times
	for row, time in zip(data_as_list,times):
		row.append(time)
		out_data_list.append(row)
	populate_data_as_list_to_csv_file(out_data_list, in_fileName)


def replace_unavailable_data_to_zero_in_csv():
	date_list = get_date_list()
	new_date_list = date_list[ date_list.index('1991-12-01') : ]
	for date in new_date_list:
		for fileName in os.listdir(SampleCSV_DIR):
			if date in fileName:
				in_fileName = os.path.join(SampleCSV_DIR, fileName)
				out_data_list = []
				out_data_list.append(HEADER[0:38])
				data_as_list = get_data_as_list(in_fileName, range(0,38))
				for row in data_as_list:
					for i in range(0,len(row)):
						if str(row[i]) == str(255):
							row[i] = 0
				out_data_list.extend(data_as_list)
				populate_data_as_list_to_csv_file(out_data_list, SampleCSV_DIR + "/" + fileName)



if __name__ == "__main__":

	in_fileName = MeanShiftResult_DIR + "/clusterCenters.csv"
	# add_average_to_cluterCenter_csv(in_fileName)

	write_times_to_clusterCenter_csv(in_fileName)
	# replace_unavailable_data_to_zero_in_csv()
