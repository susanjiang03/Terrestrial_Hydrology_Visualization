
import os
import csv
import numpy
from operator import add
from numpy import sum
import matplotlib.pyplot as plt
from GetData import *
from PopulateFiles import *
CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResult_DIR = PARENT_DIR + "/MeanShiftResult"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"





# plt.hist([1, 2, 1], bins=[0, 1, 2, 3])
# #(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
# plt.show()


# plt.hist([80, 15, 40, 33, 22, 58, 66, 30, 20], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80,90])
# #(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
# plt.show()

HEADER = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']



DATE_LIST = get_date_list()

def merge_sample_files():
	out_f = open(MeanShiftResult_DIR + '/sample.csv', 'w+')
	writer = csv.writer(out_f)
	writer.writerow(HEADER)
	the_dir = SampleCSV_DIR
	for date in DATE_LIST :
		for fileName in os.listdir(the_dir):
			if date in fileName:
				print "Write for %s"%fileName
				with open(os.path.join(the_dir,fileName), "rU") as in_f:
					reader = csv.reader(in_f)
					data_as_list = list(reader)
					# print len(data_as_list)
					for row in data_as_list[1:]:
						writer.writerow(row)
				in_f.close()
			out_f



def populate_ave_for_all_date():
	out_data_as_list = []
	# header = ['start_date', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
	# 'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
	# 'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
	# 'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
	# 'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
	# 'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
	# 'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']
	header = ['date']
	header.extend(range(0,34))
	out_data_as_list.append(header)

	for date in DATE_LIST[ DATE_LIST.index('1991-12-01') : ]:
		in_fileName = '%s/%s.csv'%(SampleCSV_DIR,date)
		data_as_list = get_data_as_list(in_fileName, range(4,38))
		total_count = len(data_as_list)
		list_of_sum = data_as_list[0]

		for row in data_as_list[1:]:
			list_of_sum = np.add(list_of_sum,row)

		list_of_ave = [ float(total/total_count) for total in list_of_sum]
		#aver for each date    indicator | average 
		newheader = ['indicator', 'average']
		out_ave_data_as_list = []
		out_ave_data_as_list.append(newheader)
		for i,data in zip(range(0,34) ,list_of_ave):
			print [i,data]
			out_ave_data_as_list.append([i,int(data)])
		out_ave_file = MeanShiftResult_DIR + "/Average/average_%s.csv"%date
		populate_data_as_list_to_csv_file(out_ave_data_as_list, out_ave_file)
		#for all dates:
		out_row = [date]
		out_row.extend(list_of_ave)
		out_data_as_list.append(out_row)
		print "get a list_of_ave:"
		print out_row

	out_total_ave_file = MeanShiftResult_DIR+ "/Average/average.csv"
	populate_data_as_list_to_csv_file(out_data_as_list, out_total_ave_file)


def populate_ave_all_dates_clusters():

	in_fileName = MeanShiftResult_DIR + "/average.csv"
	header = get_header(in_fileName);
	data_as_list = get_data_as_list(in_fileName , range(0,len(header)))
	header.append('clusters');
	out_data_as_list = []
	out_data_as_list.append(header)
	list_of_cluster_number = get_cluster_number_all_dates()
	for i in range(0, len(data_as_list)):
		data_as_list[i].append(list_of_cluster_number[i])

	out_data_as_list.extend(data_as_list)
	out_file = MeanShiftResult_DIR + "/average_clusters.csv"
	populate_data_as_list_to_csv_file(out_data_as_list, out_file)
    


def populate_ave_Land_Surface():
	in_fileName = MeanShiftResult_DIR + "/average.csv"
	header = get_header(in_fileName)
	out_data_as_list = [header[:5]]
	data_as_list = get_data_as_list(in_fileName, range(0,4))
	out_data_as_list.extend(data_as_list)
	out_file = MeanShiftResult_DIR + "/threeVar.csv"
	populate_data_as_list_to_csv_file(out_data_as_list,out_file)




def populate_ave_by_season():
	in_fileName = MeanShiftResult_DIR + "/average.csv"
	header = get_header(in_fileName)
	header[0] = "date"
	data_as_list = get_data_as_list(in_fileName , range(0,len(header)))
	seasons = ['-03-01', '-06-01', '-09-01', '-12-01']
	for season in seasons:
		out_data_as_list = []
		out_data_as_list.append(header)
		filter_data_as_list = [row for row in data_as_list if season in row[0]]
		out_data_as_list.extend(filter_data_as_list)
		out_file = MeanShiftResult_DIR + "/average_%s.csv"%season
		populate_data_as_list_to_csv_file(out_data_as_list, out_file)




def get_cluster_number_all_dates():
	in_fileName = MeanShiftResult_DIR + "/clusterCenters.csv"
	list_of_cluster_number = []
	# header = get_header(in_fileName)
	# print header
	for date in DATE_LIST[ DATE_LIST.index('1991-12-01') : ] :
		filter_data_as_list = filter_by_index_value(in_fileName, 1 , date)
		list_of_cluster_label = [int(row[0]) for row in filter_data_as_list]
		n_cluster_ = max(list_of_cluster_label) + 1
		list_of_cluster_number.append(n_cluster_)
	print list_of_cluster_number
	print max(list_of_cluster_number)
	return list_of_cluster_number




# get_cluster_number_all_dates()
# populate_ave_all_dates_clusters()





# def rewrite_cluster_label_order_by_longtitue():
# 	newHEADER = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
# 'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
# 'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
# 'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
# 'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
# 'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
# 'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2','clusterLabel']
    
# 	the_dir = SampleCSV_DIR
# 	date_list = get_date_list()
# 	start_data_index = date_list.index('1991-12-01')     
# 	#for date in ['1994-03-01', '1994-09-01', '1996-06-01']:
# 	for date in date_list[start_data_index:][ : ]:
# 		for fileName in os.listdir(the_dir):
# 			if date in fileName:
# 				print "\nChange cluster label for %s"%fileName
# 				in_fileName = os.path.join(the_dir, fileName)
# 				out_data_as_list = []
# 				out_data_as_list.append(newHEADER)
# 				header = get_header(in_fileName)
# 				data_as_list = get_data_as_list(in_fileName,range(0,len(header)))
# 				out_data_as_list.extend(data_as_list)
# 				list_of_cluster_label = [int(row[0]) for row in get_data_as_list(in_fileName,[ -1 ]) ]
# 				#print list_of_cluster_label
# 				n_cluster = max(list_of_cluster_label) + 1
# 				dict_n_ave = {}
# 				list_of_ave = []
# 				for n in range(0,n_cluster):
# 					filter_data_as_list = filter_by_index_value(in_fileName,  - 1  , str(n) )
# 					#print filter_data_as_list
# 					list_of_lat = [float(row[2]) for row in filter_data_as_list ]
# 					#print list_of_lat[:10]
# 					ave_lat = reduce(lambda x, y: x + y, list_of_lat ) / len(list_of_lat)
# 					#print ave_lat
# 					dict_n_ave[n] = ave_lat
# 					list_of_ave.append(ave_lat)
# 				list_of_ave.sort()
# 				ave_by_order = list_of_ave.sort()
# 				dict_old_new = {}
# 				for n in range(0,n_cluster):
# 					lat = dict_n_ave[n] 
# 					new_order = list_of_ave.index(lat)
# 					dict_old_new[n] = new_order
# 				print dict_old_new
# 				#rewrite the label
#                 data_as_list = get_data_as_list(in_fileName,range(0,len(header)))
#                 new_data_as_list = []
#                 new_data_as_list.append(newHEADER)
#                 change = ""
#                 for row in data_as_list[:]:
#                 	label = row[-1]
#                 	new_label = dict_old_new[label]
#                 	if label != new_label:
#                 	   print "Replace %d as %d"%(label,new_label)
#                 	   change = "Has change"
#                 	   row[-1] = new_label
#                 	   #print row
#                 	   new_data_as_list.append(row)
#                 	else:
#                 		print "No change"
#                 		new_data_as_list.append(row)
#                 # print change
#                 populate_data_as_list_to_csv_file(new_data_as_list, in_fileName)



# rewrite_cluster_label_order_by_longtitue()


def populate_ave_all_variables_for_each_date():
    in_fileName = '%s/Average/average.csv'%(MeanShiftResult_DIR)
    data_as_list = get_data_as_list(in_fileName, range(0,34))
    for date in DATE_LIST[ DATE_LIST.index('1991-12-01') : ][0]:
    	filter_data_as_list = [row[1:] for row in data_as_list if row[0] == date]
    	# print filter_data_as_list
    	print data_as_list
    	# header = ['indicator', 'Average']
    	# out_data_as_list = []
    	# out_data_as_list.append(header)
    	# for var,data in zip(HEADER[4:38], filter_data_as_list[4:38]):
	    # 	out_data_as_list.extend([var,int(data)])
    	# out_file = '%s/Average/average_%s.csv'%(MeanShiftResult_DIR,date)
    	# populate_data_as_list_to_csv_file(out_data_as_list, out_file)


if __name__ == "__main__":
	# populate_ave_all_variables_for_each_date()
	populate_ave_for_all_date()


# old = 'P0.1_N1_'
# new =  ""
# the_dir = SampleCSV_DIR 
# for fileName in os.listdir(the_dir):
# 	if old in fileName:
# 		newName = fileName.replace(old, new)
# 		#newName = fileName.replace(name, "")
# 		#print fileName
# 		os.rename(os.path.join(the_dir,fileName ), os.path.join(the_dir,newName))
# 		print "rename in %s\n%s"%(the_dir,newName) 
# 	else:
# 		print "name pattern not exits"


# import numpy as np
# import pylab as P
# #
# # first create a single histogram
# #
# mu, sigma = 200, 25
# x = mu + sigma*P.randn(10000)
# #
# # finally: make a multiple-histogram of data-sets with different length
# #
# x0 = mu + sigma*P.randn(10000)
# x1 = mu + sigma*P.randn(7000)
# x2 = mu + sigma*P.randn(3000)

# # and exercise the weights option by arbitrarily giving the first half
# # of each series only half the weight of the others:

# w0 = np.ones_like(x0)
# w0[:len(x0)/2] = 0.5
# w1 = np.ones_like(x1)
# w1[:len(x1)/2] = 0.5
# w2 = np.ones_like(x2)
# w0[:len(x2)/2] = 0.5



# P.figure()

# n, bins, patches = P.hist( [x0,x1,x2], 10, weights=[w0, w1, w2], histtype='bar')

# P.show()


# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

# from plotly import tools
# import plotly.plotly as py
# import plotly.graph_objs as go

# """
# Simple demo with multiple subplots.
# """
# import numpy as np
# import matplotlib.pyplot as plt


# fig, ax = plt.subplots(2,2)
# x1 = np.linspace(0.0, 5.0)
# x2 = np.linspace(0.0, 2.0)
# x3 = np.linspace(0.0, 5.0)
# x4 = np.linspace(0.0, 2.0)

# y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
# y2 = np.cos(2 * np.pi * x2)
# y3 = np.cos(2 * np.pi * x3) * np.exp(-x3)
# y4 = np.cos(2 * np.pi * x4)

# # plt.subplot(2, 1, 1)
# # plt.plot(x1, y1, 'ko-')
# # plt.title('A tale of 2 subplots')
# # plt.ylabel('Damped oscillation')

# # plt.subplot(2, 1, 2)
# # plt.plot(x2, y2, 'r.-')
# # plt.xlabel('time (s)')
# # plt.ylabel('Undamped')

# # plt.subplot(3, 1, 3)
# # plt.plot(x3, y3, 'ko-')
# # plt.title('A tale of 2 subplots')
# # plt.ylabel('Damped oscillation')

# # plt.subplot(4, 1, 4)
# # plt.plot(x4, y4, 'r.-')
# # plt.xlabel('time (s)')
# # plt.ylabel('Undamped')
# ax[0,0].plot(x1,y1,'ko-')
# ax[0,1].plot(x1,y1,'ko-')
# ax[1,0].plot(x1,y1,'ko-')
# ax[1,1].plot(x1,y1,'ko-')
# plt.show


# import matplotlib.pyplot as plt
# import numpy as np

# data=np.random.random((5,20))
# xaxes = ['x1','x2','x3','x4']
# yaxes = ['y1','y2','y3','y4']
# titles = ['t1','t2','t3','t4'] 

# f,a = plt.subplots(2,2)
# a = a.ravel()
# for idx,ax in enumerate(a):
# 	ax.hist(data[idx],bins=range(5,20,5))
# 	ax.set_title(titles[idx])
# 	ax.set_xlabel(xaxes[idx])
# 	ax.set_ylabel(yaxes[idx])
# plt.tight_layout()
# plt.show()

