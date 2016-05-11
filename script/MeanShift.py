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
@matrix_lat_lon_label : matrix_lat_lon_label : each row is a list of number, length 3, [lat,lon,integer_label]
@out_image_file: where to save the image,  dir + name, name must end with ("jpg","png" , ...)
                if empty, just show it. 
'''

def plot_on_baseMap_by_matrix(matrix_lat_lon_label, out_image_file):

#plot map for the file on the direct
	print "\n+++++++++ Ploting result on map: ++++++++++++++ "
	plt.figure(1)
	plt.clf()

	m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,\
	        llcrnrlon=-180,urcrnrlon=180,resolution='c')
	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()
	# m.drawrivers()
	m.fillcontinents(color='w',lake_color='#FFFFFF')
	# draw parallels and meridians.
	m.drawparallels(np.arange(-90.,91.,30.))
	m.drawmeridians(np.arange(-180.,181.,60.))
	m.drawmapboundary(fill_color='#FFFFFF')

	num_colors = len(colors_)
	n_clusters_ = 0
	for row  in matrix_lat_lon_label:
		lat = float(row[0])
		lon = float(row[1])
		x,y = m(lon,lat)
		label = row[2]
		n_clusters_ = max(n_clusters_,label)
		if label > num_colors:
			label = label%num_colors
			color = colors_[label][0]
			m.plot(x,y, markeredgecolor = color, marker='o', markersize = 2)
		else: 
			color = colors_[label][0]
			m.plot(x,y, markeredgecolor = color, marker='o', markersize = 2)

	n_clusters_ = n_clusters_ + 1
	imageName = out_image_file[out_image_file.rfind("/") + 1  : out_image_file.rfind(".")]
	imageTitle = '%s \n Estimated number of clusters: %d'%(imageName, n_clusters_) 
	plt.title(imageTitle)
	print "\nFinish ploting result on map."
    #if need to save the file
	if out_image_file != "":
		dest = out_image_file[: out_image_file.rfind("/")]
		try:
			os.makedirs(dest)
		except OSError as exc: # Guard against race condition
		    if exc.errno != errno.EEXIST:
		        raise
		    else:
		    	pass
		plt.savefig(out_image_file)
		print "\nsave file to %s."%out_image_file
	else:
		plt.show()
	plt.clf()



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
	header = get_header(in_fileName)
	data_as_list = get_data_as_list(in_fileName, range(0,len(header)))
	print data_as_list[:2]
	#if column exist , the cluster labels for this list of varialbe exist already,
	#find the index  replace
	if new_column_name in header:
		print "This Clusters Labels column exists. Update for new cluster labels."
		print new_column_name
		#keep the header
		new_data_as_list.append(header)
		theIndex = header.index(new_column_name)
		for row, label in zip(data_as_list, labels):
			#replace the label
			row[theIndex] = label
			new_data_as_list.append(row)
	else:
		header.append(new_column_name)
		new_data_as_list.append(header)
		for row, label in zip(data_as_list, labels):
			row.append(label)
			new_data_as_list.append(row)
	populate_dataList_to_csvFile(new_data_as_list,in_fileName)



# '''after labelClusters_*.csv has been populated, plot map for the existing culstering label files
# look csv file in the '/%s/LABLECSV/P%r_N%d'%(MeanShiftResut_DIR, percentage, sampleNum)
# read label csv file , then plot map base, get label data, by column name in labelcsv file
# @percentage  real number in range(0,1)
# @sampleNum  integer
# @date: string of date   eg. '1990-12-01'
# @list_of_variable  list of integer in range(4,39)
# @quantile   real number in range(0,1)

# '''
# def plot_on_baseMap_by_labelCSV(percentage,sampleNum,date,list_of_variable, quantile):

# 	#find the labe csv file
# 	in_fileName = '%s/LABELCSV/P%r_N%d/labelClusters_P%r_N%d_sample_%s.csv'%(MeanShiftResutl_DIR, percentage, sampleNum, percentage, sampleNum, date)

# #plot map for the file on the direct
# 	print "\n+++++++++ Ploting result on map: ++++++++++++++ for \n%s" %in_fileName
# 	plt.figure(1)
# 	plt.clf()



'''
does 4 things
1) run meanShift  : 
       meanShift_clustering(data_as_list,quantile)
2)plot map :
      plot_on_baseMap_by_matrix(list_lat_lon, labels, out_image_file)
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
def meanShift_clustering_writeCSV_plotMap(the_dir,date,list_of_index,quantile):
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

	# ######## (2) Append LABELS TO CSV , Append to each row in in_fileName #######################################
	#generate out_image_file_name
	str_list_of_index = ""
	list_of_index.sort()
	if list_of_index == range(4,38):
		str_list_of_index ='[ALL]'
	else:
		str_list_of_index = '[%s]'%(",".join(map(str,list_of_index)))
	new_column_name =  'V%s_Q%r_C%d'%(str_list_of_index,quantile,n_clusters_)
    #append labels
	append_labelsClusters_to_csv_file(in_fileName, new_column_name,labels)

	##########(3) WRITE CLUSTER CENTERS TO CSV in CLUSTERCENTERCSV folder #########################
	parent_folder_name = the_dir.split("/")[-1]
	out_clusters_csv_file = "%s/%s_Q%r_V%s/clusterCenters_%s"%(MeanShiftResult_CLUSTERCENTERSCSV_DIR,parent_folder_name,quantile, str_list_of_index, file_name)
	out_data_as_list = [HEADER[4:]]
	out_data_as_list.extend(cluster_centers)
	#write cluster centers
	populate_dataList_to_csvFile(out_data_as_list,out_clusters_csv_file)

	######## (4) PLOT ON MAP SAVE IMAGE TO out_image_file ###########################################
	matrix_lat_lon_label = []  
	list_lat_lon = get_data_as_list(in_fileName, range(2,4))
	for row, label in zip(list_lat_lon, labels):
		row.append(label)
		matrix_lat_lon_label.append(row)
	out_image_file = "%s/IMAGES/%s_Q%r_%s/map_%s"%(MeanShiftResult_DIR,parent_folder_name,quantile, str_list_of_index, file_name.replace(".csv","_C%d.jpg"%n_clusters_))
	#plot_on_baseMap
	#plot_on_baseMap_by_matrix(matrix_lat_lon_label, out_image_file)




if __name__ == "__main__":
  
 	list_of_date = get_date_list()   #sorted
 	new_list_of_date = list_of_date[list_of_date.index('1991-12-01'):]
 	percentage = 0.1
 	sampleNum = 1
 	quantile = 0.1
	sample_dir = "%s/P%r_N%d"%(SampleCSV_DIR, percentage,sampleNum)
	list_of_index = range(4,38)
	for date in new_list_of_date[0:3]:
		meanShift_clustering_writeCSV_plotMap(sample_dir , date, list_of_index ,quantile)









