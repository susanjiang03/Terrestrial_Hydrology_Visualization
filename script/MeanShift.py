"""
=============================================
A demo of the mean-shift clustering algorithm
=============================================

Reference:

Dorin Comaniciu and Peter Meer, "Mean Shift: A robust approach toward
feature space analysis". IEEE Transactions on Pattern Analysis and
Machine Intelligence. 2002. pp. 603-619.

"""
print(__doc__)
import sys
import csv
import os
import errno
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from itertools import cycle
from matplotlib import colors
import six
import json
import math
import numpy as np
#in the current_dir
from GetData import *
from PopulateFiles import *
from PlotImages import *

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

colors_ = list(six.iteritems(colors.cnames))*2

HEADER = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']

NUM_OF_VARIABLE = len(HEADER) - 4



'''
@data_as_list  : only cotains real numbers
@quantile  : real numbeer in range(0,1)
return arrar(labels,n_clusters,cluster_centers)
'''
def meanShift_clustering(data_as_list, quantile):

	X = np.array(data_as_list)
	###############################################################################
	# Compute clustering with MeanShift
	# The following bandwidth can be automatically detected using
	print "\n++++++++  Running Mean shift clustering algorithm for %d variables: ++++++++" %len(data_as_list[0])
	print "quantile: %r" %quantile
	bandwidth = estimate_bandwidth(X, quantile = quantile )
	ms = MeanShift(bandwidth = bandwidth, bin_seeding = True)
	#ms = MeanShift#(bin_seeding=True)
	ms.fit(X)

	labels = ms.labels_
	cluster_centers = ms.cluster_centers_

	#print cluster_centers

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)

	print "Finish running Mean shift clustering algorithm."
	print("\nnumber of estimated clusters : %d" % n_clusters_)
	return labels,n_clusters_, cluster_centers


'''
Given data_as_list, old labels, old clusterCenters
change the labels,cluster_centers order  by the ave lat of same cluster locations
return new labels, new cluster_center

'''


def find_center_lat_lon(data_as_list, labels):
	#find out the location
	dict_n_center_lat_lon = {}   # n: [lat, lon, sum_lat, sum_lon ,count]
	for row,label in zip(data_as_list,labels):
		if label not in dict_n_center_lat_lon.keys():
			list_of_value = [ float(row[2]), float(row[3]) , float(row[2]), float(row[3]) , 1 ]
			dict_n_center_lat_lon[label] = list_of_value
		else:
			list_of_value = dict_n_center_lat_lon[label]
			sum_lat = list_of_value[2] + float(row[2]) 
			sum_lon = list_of_value[3] + float(row[3]) 
			count = list_of_value[-1] + 1
			ave_lat = sum_lat / count
			ave_lon = sum_lon /count 
			new_list_of_value = [ave_lat, ave_lon, sum_lat, sum_lon , count]
			dict_n_center_lat_lon[label] = new_list_of_value
	#print dict_n_center_lat_lon
	return dict_n_center_lat_lon


def reorder_cluster_label_by_center_lat(n_clusters_, dict_n_center_lat_lon):
	list_of_center_lat = []
	for n in range(0,n_clusters_):
		lat = dict_n_center_lat_lon[n][1]
		list_of_center_lat.append(lat)
	list_of_center_lat.sort()
	dict_old_new = {}
	for key,value in dict_n_center_lat_lon.iteritems():
		lat = value[1]
		new_label = list_of_center_lat.index(lat)
		if key != new_label:
			print "Repalce old %d as new %d"%(key,new_label)
		dict_old_new[key] = new_label
	return dict_old_new

def replace_labels(dict_old_new,labels):
	new_labels = [ dict_old_new[i] for i in labels]
	return new_labels


def get_list_new_center_cluster_centers(date,n_clusters_, dict_old_new, dict_n_center_lat_lon,cluster_centers):
	new_center_cluster_centers = []
	for new in range(0,n_clusters_):
		#find old key bu new_lable
		old = [key for key, value in dict_old_new.iteritems() if value == new][0]
		center_lat_lon = dict_n_center_lat_lon[old][:2]
		new_row = [new ,date]
		new_row.extend(center_lat_lon)
		cluster_center = cluster_centers[old]
		new_row.extend(cluster_center)
		new_center_cluster_centers.append(new_row)
	return new_center_cluster_centers


def change_cluster_label_order_by_center_lat_lon(date, data_as_list,labels,cluster_centers):
    n_clusters_ = len(cluster_centers)
    dict_n_center_lat_lon = find_center_lat_lon(data_as_list,labels)
    dict_old_new = reorder_cluster_label_by_center_lat(n_clusters_, dict_n_center_lat_lon)
    new_labels = replace_labels(dict_old_new,labels)
    new_center_cluster_centers = get_list_new_center_cluster_centers(date, n_clusters_,dict_old_new,dict_n_center_lat_lon,cluster_centers)
    #list_of_location_center = get_list_of_location_center(n_clusters_,dict_old_new,cluster_centers)
    return new_labels,new_center_cluster_centers

'''
use after mean shift algorithm generate labels, and cluster_centers,
@in_fileName
@new_column_name
@labels , a list of integers
'''
def append_labelsClusters_to_csv_file(in_fileName, new_column_name,labels):

	##############################################################################
	print  "\n++++++++ Writing clusterCenters to csv file : ++++++++++"

	header = []
	new_data_as_list = []
	header = get_header(in_fileName)[:38]
	header.append(new_column_name)
	new_data_as_list.append(header)
	data_as_list = get_data_as_list(in_fileName, range(0,38))
	#if column exist , the cluster labels for this list of varialbe exist already,
	#find the index  replace
	# if new_column_name in header:
	# 	print "This Clusters Labels column exists. Update for new cluster labels."
	# 	print new_column_name
	# 	#keep the header
	# 	new_data_as_list.append(header)
	# 	theIndex = header.index(new_column_name)
	# 	for row, label in zip(data_as_list, labels):
	# 		#replace the label
	# 		row[theIndex] = label
	# 		new_data_as_list.append(row)
	# else:
	for row, label in zip(data_as_list, labels):
		if len(row) == 38:
		   row.append(label)
		if len(row) == 39:
		   row[-1] == label
		new_data_as_list.append(row)
	populate_data_as_list_to_csv_file(new_data_as_list,in_fileName)


def append_clusterCenters_to_csv_file(new_center_cluster_centers):
	in_fileName = "%s/clusterCenters.csv"%(MeanShiftResult_DIR)
	out_data_as_list = []
	newHeader = ['clusterLabel' ,'start_date']
	newHeader.extend(HEADER[2:38])
	out_data_as_list.append(newHeader)

	if not os.path.isfile(in_fileName):
		dest = in_fileName[ : in_fileName.rfind("/")]
		try:
			os.makedirs(dest)
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
			else:
				pass
		out_data_as_list.extend(new_center_cluster_centers)
	else:
		header = get_header(in_fileName)
		data_as_list = get_data_as_list(in_fileName,range(0,len(header)))
		#filtered row with same date, replace with new
		filtered_data_as_list = [ row  for row in data_as_list if row[1]!= date ]
		#print filtered_data_as_list
		out_data_as_list.extend(filtered_data_as_list)
		out_data_as_list.extend(new_center_cluster_centers)

	populate_data_as_list_to_csv_file(out_data_as_list, in_fileName)





'''
does 4 things
1) run meanShift  : 
       meanShift_clustering(data_as_list,quantile)

2) change the order of label by order the center location by lat
3)appendto csv file: 
      append_labelsClusters_to_csv_file(in_fileName,new_column_name,labels, cluster_centers, out_csv_file_name)  
4) save cluster center to csv file :
      populate_clusterCenters_to_csv_file

@ the dir : csv in the dir to choose from
@date : date '1991-12-01', '1992-03-01'
@list_of_index  list of integer in range (4,38), to clustering
@quntile : real number in (0,1)

'''

# def meanShift_clustering_writeCSV_plotMap(in_fileName,list_of_index,quantile):
def meanShift_clustering_writeCSV(the_dir,date,list_of_index,quantile):
	in_fileName = ""
	file_name = ""
	for fileName in os.listdir(the_dir):
		if fileName.endswith(date + ".csv"):
			file_name = fileName
			in_fileName = os.path.join(the_dir, fileName) 
	if in_fileName == "":
		print "Error, no csv file for %s in %s"%(date,the_dir)
		return
	####### (1) MEANSHIFT #############################################
	print "\n\nMeanShift for %s" %in_fileName
	data_as_list = get_data_as_list(in_fileName, list_of_index)
	labels, n_clusters_, cluster_centers = meanShift_clustering(data_as_list,quantile)


	####### (2) Change the label by find out the location whose values are closet to cluster centers.
	#change order the label by average lat of same clusetering row
	all_data_as_list = get_data_as_list(in_fileName,range(0,38))
	# new_labels, new_cluster_centers, list_of_location_center = 
	new_labels, new_center_cluster_centers = change_cluster_label_order_by_center_lat_lon(date, all_data_as_list,labels,cluster_centers)
	# ######## (3) Append LABELS TO CSV , Append to each row in in_fileName #######################################
    
	append_labelsClusters_to_csv_file(in_fileName, 'clusterLabel',new_labels)

	# ##########(4) WRITE CLUSTER CENTERS TO CSV in CLUSTERCENTERCSV folder #########################

	append_clusterCenters_to_csv_file(new_center_cluster_centers)


if __name__ == "__main__":
  
 	list_of_date = get_date_list()   #sorted
 	new_list_of_date = list_of_date[list_of_date.index('1991-12-01'):]
 	# percentage = 0.1
 	# sampleNum = 1
 	quantile = 0.1
	sample_dir = "%s"%(SampleCSV_DIR)
	list_of_index = range(4,38)
	for date in new_list_of_date[:1]:
		meanShift_clustering_writeCSV(sample_dir , date, list_of_index ,quantile)









