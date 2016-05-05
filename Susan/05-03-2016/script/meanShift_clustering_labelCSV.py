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
#from sklearn.datasets.samples_generator import make_blobs

currentDir = os.getcwd()
parentDir = currentDir[:currentDir.rfind("/")]
colors_ = list(six.iteritems(colors.cnames))
location_dict = {}

header = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']

num_of_variable = len(header) - 4

headerLabel = "clusteringLabel"

#return the list of all dates, in_file is pre-populated txt file
def get_date_list(in_file):
	fo = open(in_file)
	r = fo.readline()
	r = r.strip()
	dateList = r.split(" ")
	#print indexList
	return dateList

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

#in_filename is csv file name
#this function cluster
def meanShit_clustering_to_labelCSV(in_filename, list_of_variable, QUANTILE):
	print "\n========================================================================"
	filename = in_filename[in_filename.rfind("/") + 1:]
	print "get data_matrix for " +  in_filename 

	data_as_list = []
	with open(in_filename, 'rb') as in_f:
	    reader = csv.reader(in_f)
	    next(reader, None) #skip the headers
	    data_as_list = list(reader)
	in_f.close()

	filtered_data_variable_list = []
	#each row in date_matrix only contain data that need to be clustered 
	#dimention : row: len(sampleLocations) colum : len(list_of_varialbe)
	clustering_data_matrix = []  

	for row in data_as_list:
		filtered_row = row[:4]  #first 4 colums, index, date, lon, lat
		#print filtered_row
		newRow = []
		for i in list_of_variable:
		   newRow.append(int(row[i]))  #data of the variable
		#print newRow
		filtered_row.extend(newRow)   #extend varible
		filtered_data_variable_list.append(filtered_row)
		clustering_data_matrix.append(newRow)
    

	X = np.array(clustering_data_matrix)

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
	print("\nnumber of estimated clusters : %d" % n_clusters_)

	##############################################################################
	print  "\n++++++++ Writing row with label to CSV file : ++++++++++"

	str_list = map(str,list_of_variable)
	varString = "|"
	varString = varString + "|".join(str_list)
	if len(list_of_variable) == num_of_variable:
		varString = '(%d)' %num_of_variable

	out_fileName = "labelClusters_" +str(QUANTILE) + "_" + filename[:-4] +"_" + str(n_clusters_) +"_" + varString + ".csv"
	print "output fileName:" + out_fileName

	 #make dir containing VarString in dest dir
	dest = parentDir + "/MeanShiftResult"
	csvDir = dest + "/LABELCSV"
	sub_csvDir = csvDir + "/labelCSV_" + varString
	#try to make dir where to save the csv file for this clustering, dir name is (eg. "4|5")
	try:
	   os.makedirs(sub_csvDir)
	except OSError as exc: # Guard against race condition
	    if exc.errno != errno.EEXIST:
	        raise
	    else:
	    	pass

	#print "Out put direct: %s " %sub_csvDir
	output = os.path.join(sub_csvDir, out_fileName)
	out_f = open(output,'wb')
	writer = csv.writer(out_f)

	#write newHeader in first line of out file
	#in new csv file, we want columns: index | lat| lon | v1| v2 | ...
	newHeader = [] 
	newHeader.extend(header[:4])  #index
	#append variable name, and write new header to out_file
	for i in list_of_variable:
		newHeader.append(header[i])
	#last colum is cluster label number
	newHeader.append(headerLabel)
	writer.writerow(newHeader)

	for i in range(0,len(filtered_data_variable_list)):
		#write to csv file   |locationIndex | date | v1| v2| ...| labelCluster
		out_list = filtered_data_variable_list[i]
		out_list.append(labels[i])
		writer.writerow(out_list)
		print "Writing to CSV:"
		print out_list
	out_f.close()
    
	print  "Finish Writing row with label to CSV file: \n   %s" %output
	return output


# #this function must be called after generating labelCluster*.csv files 
# def plot_on_baseMap_by_variables(list_of_variable):

# 	str_list = map(str, list_of_variable)
# 	print str_list
# 	varString = "|"
# 	varString = varString + "|".join(str_list)
# 	print varString
# 	#find csv file location
# 	csvDir = currentDir + "/LABELCSV"
# 	sub_csvDir = csvDir + "/labelCSV_" + varString
# 	print "read file from %s :" %sub_csvDir
# 	#save image to location
# 	imageDir = currentDir + "/IMAGES"
# 	sub_imageDir = imageDir + "/images_" + varString
# 	print "save file to %s :"%sub_imageDir
# 	try:
# 		os.makedirs(sub_imageDir)
# 	except OSError as exc: # Guard against race condition
# 	    if exc.errno != errno.EEXIST:
# 	        raise
# 	    else:
# 	    	pass
# 	#plot for all dates that generate labelClustering csv file already
# 	for fileName in os.listdir(sub_csvDir):

# 		labelClusters_as_list = []
# 		with open(os.path.join(sub_csvDir,fileName), 'rb') as in_f:
# 			reader = csv.reader(in_f)
# 			next(reader, None) #skip the headers
# 			labelClusters_as_list = list(reader)
# 		in_f.close()

# 	#plot map for the file on the direct
# 		print "\n+++++++++ Ploting result on map: ++++++++++++++ \n for %s" %fileName
# 		plt.figure(1)
# 		plt.clf()

# 		m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,\
# 		        llcrnrlon=-180,urcrnrlon=180,resolution='c')

# 		m.drawcoastlines()

# 		m.drawcountries()
# 		m.drawstates()
# 		m.drawrivers()

# 		m.fillcontinents(color='w',lake_color='#FFFFFF')

# 		# draw parallels and meridians.

# 		m.drawparallels(np.arange(-90.,91.,30.))
# 		m.drawmeridians(np.arange(-180.,181.,60.))
# 		m.drawmapboundary(fill_color='#FFFFFF')

        
# 		n_clusters_ = int(fileName.split('_')[2])
# 		step = len(colors_) / int(math.ceil(n_clusters_ / 10.0)*10)

# 		column_names = [ header[i] for i in list_of_variable]
# 		#print column_names
# 		column_names_string = " | ".join(column_names)

# 		for row in labelClusters_as_list:
# 			#print row
# 			#row has error
# 			if len(row) < 2:
# 				continue
# 			index = row[0]
# 			labelID = int(row[-1])
# 			lat,lon = float(location_dict[index][0]), float(location_dict[index][1])
# 			x,y = m(lon,lat)
# 			if labelID > len(colors_):
# 				labelID = labelID % len(colors_)
# 			color = colors_[labelID*step][0]
# 			m.plot(x,y, markeredgecolor = color, marker='o', markersize = 2)

# 		#plt.xlabel(column_names[0]+"  " column_names[1])
# 		plt.title('%s  \n %d variables Estimated number of clusters: %d \n %s' % (fileName, len(list_of_variable), n_clusters_, column_names_string))
# 		#plt.show()
# 		#imageDir = currentDir + "/IMAGES"
# 		#sub_imageDir = imageDir + "/images_" + varString[1:]
# 		#try to make dir where to save the image file for this clustering, dir name is (eg. "4|5")

# 		pngName = fileName.replace("labelClusters","map").replace("csv",'png')
# 		#pngName = "map_"+str(QUANTILE) + "_" + str(n_clusters_) +"_"+in_filename[:-4] + ".png"
# 		plt.savefig(os.path.join(sub_imageDir,pngName))
# 		#plt.show()
# 		plt.clf()
# 		print "Finish ploting result on map.\n"


#plot for labelClustering csv file 
#this function must be called after generating labelCluster*.csv files 
#in_filename is the clustering result with culst      ...../.../labelCluster_....|v1|v2|v3
#eg.

def plot_on_baseMap_by_labelCSV(in_filename):

	fileName = in_filename[in_filename.rfind('/')+1:]
	varString = fileName[fileName.find("|") : fileName.rfind(".") ]
	#print varString
	list_string = varString.split("|")[1:]
	#print list_string
	list_of_variable = map(int,list_string)
	n_clusters_ = int(fileName.split('_')[-2])
	#step = len(colors_) / int(math.ceil(n_clusters_ / 10.0)*10)
	column_names = [ header[i] for i in list_of_variable]
	column_names_string = " | ".join(column_names)


	labelClusters_as_list = []
	with open(in_filename, 'rb') as in_f:
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

	for row in labelClusters_as_list:
		#print row
		#row has error
		if len(row) < 2:
			continue
		index = row[0]
		labelID = int(row[-1])
		lat,lon = float(row[2]), float(row[3])
		x,y = m(lon,lat)
		if labelID > len(colors_):
			labelID = labelID % len(colors_)
		#color = colors_[labelID*step][0]
		color = colors_[labelID][0]
		print "plot on map: lat:%r lon:%r color: %s" %(lat, lon, color)
		m.plot(x,y, markeredgecolor = color, marker='o', markersize = 2)


	#plt.xlabel(column_names[0]+"  " column_names[1])
	#imageTitle = '%s  \n %d variables Estimated number of clusters: %d \n %s' % (fileName, len(list_of_variable), n_clusters_, column_names_string)
	if len(list_of_variable) == num_of_variable:
		varString = '(%d)'%num_of_variable
	    imageTitle = '%s  \n %d variables Estimated number of clusters: %d \n' % (fileName, len(list_of_variable), n_clusters_ ))
	else:
		imageTitle = '%s  \n %d variables Estimated number of clusters: %d \n %s' % (fileName, len(list_of_variable), n_clusters_, column_names_string)
	plt.title(imageTitle)
	print "\n"+imageTitle
	#plt.show()
	print "\nFinish ploting result on map."
	pngName = fileName.replace("labelClusters","map").replace("csv",'jpg')
	#pngName = "map_"+str(QUANTILE) + "_" + str(n_clusters_) +"_"+in_filename[:-4] + ".png"
	dest = parentDir + "/MeanShiftResult/IMAGES"
	sub_imageDir = dest + "/images_" + varString
	try:
		os.makedirs(sub_imageDir)
	except OSError as exc: # Guard against race condition
	    if exc.errno != errno.EEXIST:
	        raise
	    else:
	    	pass
	plt.savefig(os.path.join(sub_imageDir,pngName))
	#plt.show()
	plt.clf()
	print "\nsave file to %s :"%sub_imageDir



#populate csv files and plot map 
def writeCSV_plotMap(years,list_of_variable,quantile):

	SampleCSV_dir = parentDir + "/SampleCSV"
	for fileName in os.listdir(SampleCSV_dir):
		for y in years:
			if str(y) in fileName:
				labelCsvfile = meanShit_clustering_to_labelCSV(os.path.join(SampleCSV_dir,fileName),list_of_variable,quantile)
				plot_on_baseMap_by_labelCSV(labelCsvfile)


#after label*.csv populated, plot map for the existing culstering label files 
def plotMap(list_of_variable):
	str_list = map(str,list_of_variable)
	varString = "|"
	varString = varString + "|".join(str_list)
	labelCSV_dir = parentDir + "/MeanShiftResult/LABELCSV/labelCSV_" + varString
	for filename in os.listdir(labelCSV_dir):
		plot_on_baseMap_by_labelCSV(os.path.join(labelCSV_dir, filename))

if __name__ == "__main__":

	dateList = get_date_list("dateList.txt") #116 dates
	quantile = 0.05
	#years = [2000,2001,2002]
	#years = [2000,2001,2002]
	list_of_variable =  range(4,len(header))
	# writeCSV_plotMap(dateList[-6:],list_of_variable, quantile)
	# list_of_variable_2 = [4,8]
	# writeCSV_plotMap(dateList[-20:-10],list_of_variable_2, quantile)
	# writeCSV_plotMap(years,list_of_variable,quantile)
	# plotMap(list_of_variable)




