import csv
import os
import errno
import numpy as np
import json
import math
import datetime
from GetData import *
from FilterData import *
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
# def plot_histogram_by_csv_file(the_dir,date, bins, out_image_file):
# 	date_list = get_date_list()
# 	start_date_index = date_list.index('1991-12-01')
# 	new_date_list = date_list[start_date_index:]
# 	for d in new_date_list:
# 		in_fileName = '%s/P0.1_N1/P0.1_N1_%s.csv'%(SampleCSV_DIR, d)
# 		for i in range(4,38):
# 			    header = get_header(in_fileName)
# 			    index = len(header) - 1
# 			    column_name = header[-1]
# 			    n_clusters_ = int(column_name[column_name.rfind('C') + 1 :])
# 			    #plot for each cluster 
# 			    for c in range(0,n_clusters_):
# 					data_as_list = filter_by_index_value(in_fileName,index,c)
# 					plot_data = []
# 					for row in data_as_list:
# 						plot_data.append(int(row[i]))
# 					#print plot_data
# 					print len(plot_data)
# 					#print plot_data
# 					#plot_data_freq = map(lambda x: float(x/total_num),plot_data)
# 					#print plot_data_freq
# 					plt.figure(1)
# 					plt.clf()
# 					plt.hist(plot_data, bins= range(0,95,5))
# 					title = 'Histogram for Cluster %d on variable[%d] %s on %s\n'%(c,i,HEADER[i],d)
# 					plt.title(title)
# 					print title
# 					#(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
# 					dest = '%s/HISTOGRAMS/P0.1_N1_Q0.1_[ALL]/%s/C%d'%(MeanShiftResult_DIR,d,c)
# 					try:
# 						os.makedirs(dest)
# 					except OSError as exc: # Guard against race condition
# 						if exc.errno != errno.EEXIST:
# 							raise
# 						else:
# 							pass
# 					imageName = '%s/C%d_V%d_.jpg'%(dest,c,i)
# 					plt.savefig(os.path.join(dest,imageName))
# 					#plt.show()
# 					plt.clf()
# 					print "save to %s:  \n%s"%(dest, imageName)
	


# if __name__ == "__main__":

# 	date_list = get_date_list()
# 	start_date_index = date_list.index('1995-03-01')
# 	new_date_list = date_list[start_date_index:]
# 	for d in new_date_list[0:1]:
# 		in_fileName = '%s/P0.1_N1/P0.1_N1_%s.csv'%(SampleCSV_DIR, d)
# 		data_as_list = get_data_as_list(in_fileName,range(4,38))
# 		for i in range(4,34):
# 		    #plot for all data for 34 varialbes
# 			plot_data = []
# 			for row in data_as_list:
# 				plot_data.append(int(row[i-4]))
# 			#print plot_data
# 			print len(plot_data)
# 			plt.figure(1)
# 			plt.clf()
# 			plt.hist(plot_data, bins= range(0,95,5))
# 			title = 'Histogram for all sample locations on all %d variables on %s\n'%(len(range(4,38)),d)
# 			plt.title(title)
# 			print title
# 			#(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
# 			dest = '%s/HISTOGRAMS/P0.1_N1_Q0.1_[ALL]/%s/allLocations'%(MeanShiftResult_DIR,d)
# 			try:
# 				os.makedirs(dest)
# 			except OSError as exc: # Guard against race condition
# 				if exc.errno != errno.EEXIST:
# 					raise
# 				else:
# 					pass
# 			imageName = '%s/allLocations_V%d_.jpg'%(dest,i)
# 			plt.savefig(os.path.join(dest,imageName))
# 			#plt.show()
# 			plt.clf()
# 			print "save to %s:  \n%s"%(dest, imageName)
	





    


