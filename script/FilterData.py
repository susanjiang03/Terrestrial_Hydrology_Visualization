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
		print "Finished"
	in_f.close()
	return data_as_list
	# else: 


'''
read in_fileName, filter by index, 
@in_fileName: csv file
@index : the column index in the data
@value : filter by the value, value must be convert to string
exclude header
return a list of row
'''
def filter_by_index_value(in_fileName, index, value):
    #if index not in locationlist
	data_as_list = []
	with open(in_fileName, 'rU') as in_f:
		datareader = csv.reader(in_f)
		data_as_list = list(datareader)[1:]
	in_f.close()
	filtered_data_as_list = [ row for row in data_as_list if str(row[index]) == str(value) ]

	# with open(in_fileName, 'rb') as in_f:
	# 	datareader = csv.reader(in_f)
	# 	header = datareader.next()
	# 	next(datareader, None)
	# 	#print "\nStart filtering data for index %d in file: \n%s"%(index,in_fileName)
	# 	for line in datareader:
	# 		if int(line[index]) == value:
	# 			data_as_list.append(line)
	# in_f.close()
	#print "Finished filtering.Total number of rows is :%d"%len(data_as_list)
	return filtered_data_as_list


# if __name__ == "__main__":
# 	in_fileName = SampleCSV_DIR + "/1991-12-01.csv"
# 	for i in range(0,1):
# 	    filter_data_as_list = filter_by_index_value(in_fileName, 38 , str(i))
# 	    # print filter_data_as_list
# 	    data_as_list = [ row[5] for row in filter_data_as_list]
# 	    out_file = MeanShiftResult_DIR + "/" + "HISTOGRAMS/1991-12-01-" + str(i) + ".csv"
# 	    populate_data_as_list_to_csv_file(data_as_list, out_file)


# 	with open('indicators','rU') as in_f:
		

	# date_list = get_date_list()
	# start_date_index = date_list.index('1991-12-01')
	# new_date_list = date_list[start_date_index:]
	# for d in new_date_list:
	# 	in_fileName = '%s/P0.1_N1/P0.1_N1_%s.csv'%(SampleCSV_DIR, d)
	# 	for i in range(4,38):
	# 		    header = get_header(in_fileName)
	# 		    index = len(header) - 1
	# 		    column_name = header[-1]
	# 		    n_clusters_ = int(column_name[column_name.rfind('C') + 1 :])
	# 		    #plot for each cluster 
	# 		    for c in range(0,n_clusters_):
	# 				data_as_list = filter_by_index_value(in_fileName,index,c)
	# 				plot_data = []
	# 				for row in data_as_list:
	# 					plot_data.append(int(row[i]))
	# 				#print plot_data
	# 				print len(plot_data)
	# 				#print plot_data
	# 				#plot_data_freq = map(lambda x: float(x/total_num),plot_data)
	# 				#print plot_data_freq
	# 				plt.figure(1)
	# 				plt.clf()
	# 				plt.hist(plot_data, bins= range(0,95,5))
	# 				title = 'Histogram for Cluster %d on variable[%d] %s on %s\n'%(c,i,HEADER[i],d)
	# 				plt.title(title)
	# 				print title
	# 				#(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
	# 				dest = '%s/HISTOGRAMS/P0.1_N1_Q0.1_[ALL]/%s/C%d'%(MeanShiftResult_DIR,d,c)
	# 				try:
	# 					os.makedirs(dest)
	# 				except OSError as exc: # Guard against race condition
	# 					if exc.errno != errno.EEXIST:
	# 						raise
	# 					else:
	# 						pass
	# 				imageName = '%s/C%d_V%d_.jpg'%(dest,c,i)
	# 				plt.savefig(os.path.join(dest,imageName))
	# 				#plt.show()
	# 				plt.clf()
	# 				print "save to %s:  \n%s"%(dest, imageName)
	





    


