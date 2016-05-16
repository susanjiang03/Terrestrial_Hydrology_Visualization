import csv
import os
import errno
import numpy as np
import json
import math
import datetime
import matplotlib.pyplot as plt
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from GetData import *
from FilterData import *
from PopulateFiles import *



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

'''
@ plot_data_list: a list of numbers
@ bins, the range in x aix of histogram e.g.[0,10,20]
@ out_image_file : where to save the image : the dir + fileName
                 if empty, just show. 
'''

def plot_histogram(plot_data_list,bins,out_image_file):
	plt.figure(1)
	plt.clf()
	plt.hist(plot_data_list, bins=bins)
	if out_image_file == "":
		plt.show()
	else:
		#(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
		dest = out_image_file[:out_image_file.rfind("/")]
		try:
			os.makedirs(dest)
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
			else:
				pass
		title = out_image_file.split('/')[-1].replace(".jpg", "")
		plt.title(title)
		imageName = out_image_file.split('/')[-1]
		plt.savefig(os.path.join(dest,imageName))
		print "save to %s:  \n%s"%(dest, imageName)
		plt.clf()



def plot_histogram_on_date_index_all(the_dir,date,index,bins):
	in_fileName = ""
	for fileName in os.listdir(the_dir):
		if fileName.endswith(date + ".csv"):
			in_fileName = os.path.join(the_dir,fileName)		#all data
	if in_fileName == "":
		return "Error. file not exists."
	else:
		plot_data = get_data_as_list(in_fileName,[index])
		#print plot_data
		out_dir = '%s/HISTOGRAMS/P0.1_N1_Q0.1_V[ALL]/ALL/%s'%(MeanShiftResult_DIR ,date)
		imageName = 'allLocations_V%d_%s.jpg'%(index,date)
		plot_histogram(plot_data,bins,os.path.join(out_dir,imageName)) 


# def plot_histogram_on_date_index_all(the_dir,date,list_of_index,bins):
# 	in_fileName = ""
# 	for fileName in os.listdir(the_dir):
# 		if fileName.endswith(date + ".csv"):
# 			in_fileName = os.path.join(the_dir,fileName)		#all data
# 	if in_fileName == "":
# 		return "Error. file not exists."
# 	else:
# 		f,a = plt.subplots(2,2)
# 		a = a.ravel()
# 		for idx,ax in enumerate(a):
# 			for index in list_of_index:
# 				data_as_list = get_data_as_list(in_fileName,[index])
# 				plot_data = [row[0] for row in data_as_list][0:10]
# 				print plot_data
# 				ax.hist(plot_data,bins)
# 		plt.tight_layout()
# 		plt.show()

# def populate
def plot_histogram_on_date_index_cluster(the_dir,date,index,cluster_lable_column_name_starts_with,bins):
	for fileName in os.listdir(the_dir):
		if fileName.endswith(date + ".csv"):
			in_fileName = os.path.join(the_dir,fileName)
			header = get_header(in_fileName)
			cluster_label_column_name = ""
			for h in header:
				if h.startswith(cluster_lable_column_name_starts_with):
					cluster_label_column_name = h
					names = cluster_label_column_name.split('C')
					n_clusters_ = int(names[-1])
					cluster_label_column_index = header.index(h)
					for c in range(0,n_clusters_):
						filtered_data_as_list = filter_by_index_value(in_fileName,cluster_label_column_index,n_clusters_)
						plot_data_list = [row[index] for row in filtered_data_as_list]
						parent_dir = the_dir.split("/")
						out_dir = '%s/HISTOGRAMS/P0.1_N1_Q0.1_V[ALL]/%s/C%d'%(MeanShiftResult_DIR ,date,c)
						imageName = 'V%dC%d_%s.jpg'%(c,index,date)
						print "plot histogram for %s"%imageName
						plot_histogram(plot_data_list,bins,os.path.join(out_dir,imageName))



# def get_histogram_list_of_counts_index(in_fileName, index,date):
# 	data_as_list = get_data_as_list(in_fileName,range(0,38))
# 	#print data_as_list
# 	filtered_data_as_list = [row for row in data_as_list if row[1] == date]
# 	#print filtered_data_as_list[:3]
# 	list_of_counts = []
# 	n = 0
# 	while n < 95:
# 		list_of_row = [row for row in filtered_data_as_list if int(row[index]) in range( n , n + 5)]
# 		count = len(list_of_row)
# 		list_of_counts.append(count)
# 		n = n + 5
# 	print list_of_counts
# 	return list_of_counts


def populate_all_histogram_data_to_csv_file(the_dir, list_of_date, out_csv_file):
	dest = out_csv_file[ : out_csv_file.rfind("/")]
	try:
		os.makedirs(dest)
	except OSError as exc: # Guard against race condition
		if exc.errno != errno.EEXIST:
			raise
		else:
			pass
	out_f = open(out_csv_file, 'w+')
	writer = csv.writer(out_f)
	newHeader = ['range', 'start_date', 'cluster_name', 'clusters', ]
	newHeader.extend(HEADER[4:])
	#writer.writerow(header)
	# list_of_range = [(n , n + 5) for n in range(0,100,5)]
	# header.extend(list_of_range)
	writer.writerow(newHeader)
	for fileName in os.listdir(the_dir):
		for date in list_of_date:
			if date in fileName:
				print "populate histogram data for %s"%date
				in_fileName = os.path.join(the_dir,fileName)
				r = 0
				while r < 95:
					#for all data: 
					  #first four column,
					out_row = [ r,  date ,  "-", "-"]
					for i in range(4,38):
						filtered_data_as_list  = get_data_as_list(in_fileName,[i])
						#filtered_data_as_list = [row[i] for row in data_as_list if row[1] == date]
						list_of_days = [day for day in filtered_data_as_list if day in range( r , r + 5)]
						count = len(list_of_days)
						out_row.append(count)
					#print out_row
					writer.writerow(out_row)
					r = r + 5

					#n_cluster
					list_of_label_row = get_data_as_list(in_fileName,[-1])
					n_clusters_ = max([row[0] for row in list_of_label_row]) + 1
					r = 0
					while r < 95:
						for n in range(0,n_clusters_):
							out_row = [r,  date ,  'All' , n]
							filtered_cluster_data_as_list = filter_by_index_value(in_fileName, -1, str(n))
							for i in range(4,38):
								filtered_data_as_list  = [ row[i] for row in filtered_cluster_data_as_list ] 
								#filtered_data_as_list = [row[i] for row in data_as_list if row[1] == date]
								list_of_days = [day for day in filtered_data_as_list if day in range( r , r + 5)]
								count = len(list_of_days)
								out_row.append(count)
							#print out_row
							writer.writerow(out_row)
						r = r + 5



				

	#populate_data_as_list_to_csv_file(out_data_as_list, out_csv_file)







# if __name__ == "__main__":
	# the_dir = SampleCSV_DIR
	# bins = range(0,5,95)
	# cluster_label_column_name_starts_with = 'clusterLabel'
	# date_list = get_date_list()
	# start_date_index = date_list.index('1991-12-01')
	# new_date_list = date_list[start_date_index:][:]
	# # for date in new_date_list[0:1]:
	# # 	for index in range(4,38)[1:]:
	# # 		#by clusters
	# # 		plot_histogram_on_date_index_cluster(the_dir,date,index,cluster_label_column_name_starts_with,bins)
	# # 		#all data
	# # 		plot_histogram_on_date_index_all(the_dir,date,index,bins)
	# out_histogramCSV_file = "%s/histogramData.csv"%(MeanShiftResult_DIR)
	# # for date in new_date_list[0:1]:
 #    	#plot_histogram_on_date_index_cluster(the_dir,date,index,cluster_lable_column_name_starts_with,bins):
	# 	# for index in range(4,38):
	# 		#plot_histogram_on_date_index_cluster(the_dir,date,index,cluster_label_column_name_starts_with,bins)
	# #in_fileName = SampleCSV_DIR + "/P0.1_N1/P0.1_N1_1991-12-01.csv"
	# # print get_histogram_list_of_counts_index(in_fileName, 4 , '1991-12-01')
	# populate_all_histogram_data_to_csv_file(the_dir, new_date_list[:1], out_histogramCSV_file)







    


