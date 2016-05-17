import csv
import os
import errno
import numpy as np
from math import sqrt
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


COLORS = ['#4B0082', '#FFD700', '#FF69B4', '#B22222', '#CD5C5C', '#87AE73', '#FFFF00', '#FFE4E1','#556B2F', 
'#808000', '#8FBC8F', '#FFC0CB', '#FF6347', '#F08080', '#FF4500', '#FFDEAD', '#00FF00', '#98FB98', '#2F4F4F', 
'#ADFF2F', '#DEB887', '#FFF5EE', '#00FA9A', '#FF00FF', '#FFEFD5', '#FFEBCD', '#7FFF00', '#696969']



'''
@matrix_lat_lon_label    a list of row [lat, lon, label ] label is color number
@out_image_file  : if empyt , just show picture

'''

def plot_on_baseMap_by_matrix(matrix_lat_lon_label, clusterCenters,out_image_file):

#plot map for the file on the direct
	print "\n+++++++++ Ploting result on map: ++++++++++++++ "
	# fig = plt.figure(figsize=(27, 18))
	plt.figure(1)
	plt.clf()
	m = Basemap(projection='mill',llcrnrlat=-10,urcrnrlat=90,\
	        llcrnrlon=-180,urcrnrlon=180,resolution='c')
	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()
	# m.drawrivers()
	m.fillcontinents(color='w',lake_color='#FFFFFF')
	# draw parallels and meridians.
	m.drawparallels(np.arange(-30.,91.,20.))
	m.drawmeridians(np.arange(-180.,181.,20.))
	m.drawmapboundary(fill_color='#FFFFFF')

	num_colors = len(colors_)
	# n_clusters_ = 0
	dict_n_color = {}
	for row in matrix_lat_lon_label:
		lat = float(row[0])
		lon = float(row[1])
		x,y = m(lon,lat)
		label = row[2]
		# n_clusters_ = max(n_clusters_,label) 
		if label > num_colors:
			label = label%num_colors
			#color = colors_[label][0]
			color = COLORS[label]
			dict_n_color[label] = color
			m.plot(x,y, markeredgecolor = color, marker='o', markersize = 2)
		else: 
			color = colors_[label][0]
			dict_n_color[label] = color
			m.plot(x,y, markeredgecolor = color, marker='o', markersize = 2)
	# #cluster 
	# for row  in clusterCenters:
	# 	lat = float(row[0])
	# 	lon = float(row[1])
	# 	x,y = m(lon,lat)
	# 	label = int(row[2])
	# 	time = float(row[-1])
	# 	color = dict_n_color[label]
	# 	m.plot(x,y, markeredgecolor = color, marker='o', markersize = 10*sqrt(time))

	# n_clusters_ = n_clusters_ + 1
	# imageName = out_image_file[out_image_file.rfind("/") + 1  : out_image_file.rfind(".")]
	# imageTitle = '%s \n Estimated number of clusters: %d'%(imageName, n_clusters_) 
	# imageTitle = 'Estimated number of clusters: %d'%(n_clusters_) 
	#plt.title(imageTitle)
	print "\nFinish ploting result on map."
    #if need to save the file
	if out_image_file != "":
		dest = out_image_file[: out_image_file.rfind("/")]
		# try:
		# 	os.makedirs(dest)
		# except OSError as exc: # Guard against race condition
		#     if exc.errno != errno.EEXIST:
		#         raise
		#     else:
		#     	pass
		plt.savefig(out_image_file,bbox_inches='tight')
		print "\nsave file to %s."%out_image_file
	else:
		plt.show()
	plt.clf()


	'''
after labelClusters_*.csv has been populated, plot map for the existing culstering label files
look csv file in the '/%s/LABLECSV/P%r_N%d'%(MeanShiftResut_DIR, percentage, sampleNum)
read label csv file , then plot map base, get label data, by column name in labelcsv file
@percentage  real number in range(0,1)
@sampleNum  integer
@date: string of date   eg. '1990-12-01'
@list_of_variable  list of integer in range(4,39)
@quantile   real number in range(0,1)

'''
# def plot_on_baseMap_from_csv_file(percentage,sampleNum,date,list_of_variable, quantile):


'''
by gather data of lat,lon, label from  csv file 

list_of_index is the list of index of date, lat, lon ,label in the file 

'''

def plot_on_baseMap_from_csv_file(in_fileName, list_of_index, date, clusterCenters, out_image_file):
	#find the labe csv file
	data_as_list = get_data_as_list(in_fileName, list_of_index)
	#filter_data_as_list = [ row[1:] for row in data_as_list if row[0] == date]
	plot_on_baseMap_by_matrix(data_as_list, clusterCenters, out_image_file)
#plot map for the file on the direct
	print "\n+++++++++ Ploting result on map: ++++++++++++++ for \n%s" %in_fileName
	plt.figure(1)
	plt.clf()



def  plot_on_baseMap_on_clusterCenter():
    in_fileName = MeanShiftResult_DIR + "/clusterCenters.csv"
    data_as_list = get_data_as_list(in_fileName,[1,3,4,0,-1])
    date_list = get_date_list()
    new_date_list = date_list[ date_list.index('1991-12-01') : ]
    for date in new_date_list:
		print "\n+++++++++ Ploting result on map: ++++++++++++++ "
		filter_data_as_list = [row for row in data_as_list if row[0] == date]
		for row in filter_data_as_list:	
			# fig = plt.figure(figsize=(27, 18))
			plt.figure(1)
			plt.clf()

			m = Basemap(projection='mill',llcrnrlat=-10,urcrnrlat=90,\
			        llcrnrlon=-180,urcrnrlon=180,resolution='c')
			m.drawcoastlines()
			m.drawcountries()
			m.drawstates()
			# m.drawrivers()
			m.fillcontinents(color='w',lake_color='#FFFFFF')
			# draw parallels and meridians.
			m.drawparallels(np.arange(-30.,91.,20.))
			m.drawmeridians(np.arange(-180.,181.,20.))
			m.drawmapboundary(fill_color='#FFFFFF')

			num_colors = len(colors_)
			n_clusters_ = 0
			for row  in filter_data_as_list:
				lat = float(row[1])
				lon = float(row[2])
				x,y = m(lon,lat)
				label = int(row[3])
				time = float(row[-1])
				n_clusters_ = max(n_clusters_,label)
				if label > num_colors:
					label = label%num_colors
					# color = colors_[label][0]
					color = COLORS[label]
					m.plot(x,y, markeredgecolor = color, marker='o', markersize = 10*sqrt(time))
				else: 
					color = colors_[label][0]
					m.plot(x,y, markeredgecolor = color, marker='o', markersize = 10*sqrt(time))

			n_clusters_ = n_clusters_ + 1
			# imageName = out_image_file[out_image_file.rfind("/") + 1  : out_image_file.rfind(".")]
			# imageTitle = '%s \n Estimated number of clusters: %d'%(imageName, n_clusters_) 
			# imageTitle = 'Estimated number of clusters: %d'%(n_clusters_) 
			imageTitle = date
			plt.title(imageTitle)
			print "\nFinish ploting result on map."
	    #if need to save the file
			out_image_file = MeanShiftResult_DIR + "/clusterCenterMaps/" + date + ".jpg"
			if out_image_file != "":
				dest = out_image_file[: out_image_file.rfind("/")]
				# try:
				# 	os.makedirs(dest)
				# except OSError as exc: # Guard against race condition
				#     if exc.errno != errno.EEXIST:
				#         raise
				#     else:
				#     	pass
				plt.savefig(out_image_file,bbox_inches='tight')
				print "\nsave file to %s."%out_image_file
			else:
				plt.show()
			plt.clf()


# if __name__ == "__main__":

    # list_of_colors = [ str(row[1]) for row in colors_[:28]]
    # print list_of_colors


	# date_list = get_date_list()
	# new_date_list = date_list[ date_list.index('1991-12-01') :]
	#in_fileName = MeanShiftResult_DIR + "/clusterCenters.csv"
	#plot_on_baseMap_from_csv_file(in_fileName, [1,3,4 ,0], '1991-12-01', "")
	# plot_on_baseMap_on_clusterCenter()
	# for date in new_date_list:
	# 	for fileName in os.listdir(SampleCSV_DIR + "_2"):
	# 		if date in fileName:
	# in_fileName = os.path.join(SampleCSV_DIR + "_2" ,fileName)
	# out_image_file = MeanShiftResult_DIR + '/Maps/' + date + ".jpg"
	# plot_on_baseMap_from_csv_file(in_fileName, [2, 3 , -1], date, out_image_file)
	# in_dir = SampleCSV_DIR
	# out_dir = MeanShiftResult_DIR + "/Maps"
	# for date in new_date_list [:]:
	# 	for fileName in os.listdir(in_dir):
	# 		if date in fileName:
	# 			in_fileName = os.path.join(in_dir, fileName)
	# 			clusterCenters_fileName = MeanShiftResult_DIR + "/clusterCenters.csv"
	# 			clusterCenters_data = get_data_as_list(clusterCenters_fileName,[1 ,2,3,0,-1])
	# 			clusterCenters = [row[1:] for row in clusterCenters_data if row[0] == date]
	# 			plot_on_baseMap_from_csv_file(in_fileName, [2,3,-1], date, clusterCenters, os.path.join(out_dir, fileName.replace(".csv" , ".jpg")))




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
	





    


