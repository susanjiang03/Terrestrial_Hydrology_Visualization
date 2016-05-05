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
from matplotlib import colors

import sys
import csv
import os
import errno
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from itertools import cycle
import six
import json
#from sklearn.datasets.samples_generator import make_blobs

currentDir = os.getcwd()
colors_ = list(six.iteritems(colors.cnames))
location_dict = {}

header = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']

headerIndex = header[0]
headerLat = header[2]
headerLon = header[3]
headerLabel = "clusteringLabel"

#in_filename is a csv file filtered by date, format will be "1980-03-01.csv" or "sample_1980-03-01.csv"
#list_of_ variable = [v1,v2, ...] v in ramge[4,34] , represents different variable column index
#eg. list_of_varaible = [4,8] means it is tocluster for variable ft_frzone and fw_fw_06_swe_-3

sampleLocations_txtFile = "sampleLocations.txt"

#in_file is pre-populated txt file of sample locations index
#return a list of location index
def get_sample_locations_list(in_file):
	fo = open(in_file)
	r = fo.readline()
	r = r.strip()
	indexList = r.split(" ")
	#print indexList
	sample_indexList = map(int, indexList)
	return sample_indexList

#json_file is pre-populate json file 
#return a dictionay with key is location index, and value is tuple(lat,lon)
def get_location_dict(json_file):
	d = {}
	json_data = open("indexLocation_dict.json",'r')
	d = json.load(json_data)
	json_data.close()
	return d

def get_data_matrix(in_filename, list_of_variable):

	print "\n========================================================================"
	print "get data_matrix for " +  in_filename 

	data_as_list = []
	with open(in_filename, 'rb') as in_f:
	    reader = csv.reader(in_f)
	    next(reader, None) #skip the headers
	    data_as_list = list(reader)
	in_f.close()

    #each row in date_matrix only contain data that need to be clustered 
    #dimention : row: len(sampleLocations) colum : len(list_of_varialbe)
	data_matrix = []   

	for row in data_as_list:
		newRow = []
		for i in list_of_variable:
		   newRow.append(int(row[i]))  #data of the variable
		#print newRow
		data_matrix.append(newRow)

	return data_matrix


def meanShit_clustering_to_labelCSV(in_filename, list_of_varible, QUANTILE):
    
	#get sample location index 
	last = currentDir.rfind("/")
    txt_file = currentDir[:last] + "/script/sampleLocations.txt"
	locationIndex_list = get_sample_locations_list(txt_file)
	data_matrix = get_data_matrix(in_filename,list_of_variable)

	str_list = map(str,list_of_variable)
	varString = "|"
	varString = varString + "|".join(str_list)
	 #make dir of VarString in dest dir
	csvDir = currentDir + "/LABELCSV"
	sub_csvDir = csvDir + "/labelCSV_" + varString
	#try to make dir where to save the csv file for this clustering, dir name is (eg. "4|5")
	try:
	   os.makedirs(sub_csvDir)
	except OSError as exc: # Guard against race condition
	    if exc.errno != errno.EEXIST:
	        raise
	    else:
	    	pass
	X = np.array(data_matrix)

	###############################################################################
	# Compute clustering with MeanShift
	# The following bandwidth can be automatically detected using
	print "\n++++++++  Running Mean shift clustering algorithm: ++++++++"
	bandwidth = estimate_bandwidth(X, quantile= QUANTILE)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	#ms = MeanShift#(bin_seeding=True)
	ms.fit(X)

	labels = ms.labels_
	cluster_centers = ms.cluster_centers_

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)

	print "Finish running Mean shift clustering algorithm."
	print("number of estimated clusters : %d" % n_clusters_)

	##############################################################################
	print  "\n++++++++ Writing row with label to CSV file : ++++++++++"

	out_fileName = "labelClusters_" +str(QUANTILE) + "_" + str(n_clusters_) + "_" + in_filename[:-4] + varString + ".csv"
	print "output fileName:" + out_fileName

	output = os.path.join(sub_csvDir, out_fileName)
	out_f = open(output,'wb')
	writer = csv.writer(out_f)

	#write newHeader in first line of out file
	#in new csv file, we want columns: index | lat| lon | v1| v2 | ...
	newHeader = [] 
	newHeader.append(headerIndex)  #index
	#append variable name, and write new header to out_file
	for i in list_of_variable:
		newHeader.append(header[i])
	#last colum is cluster label number
	newHeader.append(headerLabel)
	writer.writerow(newHeader)

	for i in range(0,len(data_matrix)):
		#write to csv file   |locationIndex | labelCluster
		out_list = [locationIndex_list[i],labels[i]]
		print out_list
		writer.writerow(out_list)
    
	print  "Finish Writing row with label to CSV file: \n   %s" %output


#this function must be called after generating labelCluster*.csv files 
def plot_on_baseMap_by_variables(list_of_variable):

	str_list = map(str, list_of_variable)
	print str_list
	varString = "|"
	varString = varString + "|".join(str_list)
	print varString
	#find csv file location
	csvDir = currentDir + "/LABELCSV"
	sub_csvDir = csvDir + "/labelCSV_" + varString
	print "read file from %s :" %sub_csvDir
	#save image to location
	imageDir = currentDir + "/IMAGES"
	sub_imageDir = imageDir + "/images_" + varString
	print "save file to %s :"%sub_imageDir
	try:
		os.makedirs(sub_imageDir)
	except OSError as exc: # Guard against race condition
	    if exc.errno != errno.EEXIST:
	        raise
	    else:
	    	pass
	#plot for all dates that generate labelClustering csv file already
	for fileName in os.listdir(sub_csvDir):

		labelClusters_as_list = []
		with open(os.path.join(sub_csvDir,fileName), 'rb') as in_f:
			reader = csv.reader(in_f)
			next(reader, None) #skip the headers
			labelClusters_as_list = list(reader)
		in_f.close()

	#plot map for the file on the direct
		print "\n+++++++++ Ploting result on map: ++++++++++++++ \n for %s" %fileName
		plt.figure(1)
		plt.clf()

		m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,\
		        llcrnrlon=-180,urcrnrlon=180,resolution='c')

		m.drawcoastlines()

		m.drawcountries()
		m.drawstates()
		m.drawrivers()

		m.fillcontinents(color='w',lake_color='#FFFFFF')

		# draw parallels and meridians.

		m.drawparallels(np.arange(-90.,91.,30.))
		m.drawmeridians(np.arange(-180.,181.,60.))
		m.drawmapboundary(fill_color='#FFFFFF')

        
		n_clusters_ = int(fileName.split('_')[2])
		column_names = [ header[i] for i in list_of_variable]
		#print column_names
		column_names_string = " | ".join(column_names)

		for row in labelClusters_as_list:
			#print row
			#row has error
			if len(row) < 2:
				continue
			index = row[0]
			labelID = int(row[1])
			lat,lon = float(location_dict[index][0]), float(location_dict[index][1])
			x,y = m(lon,lat)
			if labelID > len(colors_):
				labelID = labelID % len(colors_)
			color = colors_[labelID][0]
			m.plot(x,y, markeredgecolor = color, marker='o', markersize = 2)

		#plt.xlabel(column_names[0]+"  " column_names[1])
		plt.title('%s  \n %d variables Estimated number of clusters: %d \n %s' % (fileName, len(list_of_variable), n_clusters_, column_names_string))
		#plt.show()
		#imageDir = currentDir + "/IMAGES"
		#sub_imageDir = imageDir + "/images_" + varString[1:]
		#try to make dir where to save the image file for this clustering, dir name is (eg. "4|5")

		pngName = fileName.replace("labelClusters","map").replace("csv",'png')

		#pngName = "map_"+str(QUANTILE) + "_" + str(n_clusters_) +"_"+in_filename[:-4] + ".png"
		plt.savefig(os.path.join(sub_imageDir,pngName))
		#plt.show()
		plt.clf()
		print "Finish ploting result on map.\n"


#datafile = "sample_2000-03-01.csv"
list_of_variable =  [9,14]
#QUANTILE = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8,0.9]
quantiles = [0.25]
#years = [2000,2001,2002]
years = [2000,2001,2002,2003,2004,2005,2006,2007]

Q = 0.25

#for q in QUANTILE:
#for fileName in os.listdir(os.getcwd()):
# for y in years:
# 	#if fileName.startswith("sample_"+str(y)):
# 	#if fileName == "sample_2000-03-01.csv":
# 		#for q in quantiles:    
# 	    #meanShit_clustering_labelCSV(fileName,list_of_variable)
# 	plot_on_baseMap(y,list_of_variable)

#global value 
#get location lat lon dictionary
last = currentDir.rfind("/")
json_file = currentDir[:last] + "/script/indexLocation_dict.json"
print json_file

location_dict = get_location_dict(json_file)

for fileName in os.listdir(os.getcwd()):
	for y in years:
	    if fileName.startswith("sample_"+str(y)):
	      # meanShit_clustering_to_labelCSV(fileName,list_of_variable,Q)
	        plot_on_baseMap_by_variables(list_of_variable)


