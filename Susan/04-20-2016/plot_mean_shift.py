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
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
#from sklearn.datasets.samples_generator import make_blobs

#first_arg = sys.argv[0]
# Ssecond_arg = sys.argv [1]

header = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']

#def mean_shift(in_filename=first_arg, list_of_variable=second_arg):
def mean_shiftf_clustering(in_filename, list_of_variable):

	#in_filename = "date_2005-12-01.csv"
	data_as_list = []
	column_names =[]
	with open(in_filename, 'rb') as f:
	    reader = csv.reader(f)
	    next(reader, None) 
	    data_as_list = list(reader)

	data_matrix = []

	for row in data_as_list:
		new = []
		for v in list_of_variable:
		   new.append(row[v])
		   column_names.append(header[v])

		new = map(int,new)
		data_matrix.append(new)
		

	# data_sample = data_matrix[:10000]
	data_sample = data_matrix[:10000]
	X = np.array(data_sample)

	###############################################################################
	# Compute clustering with MeanShift

	# The following bandwidth can be automatically detected using
	bandwidth = estimate_bandwidth(X, quantile=0.2)

	#ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	ms = MeanShift(bin_seeding=True)
	ms.fit(X)
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)

	print("number of estimated clusters : %d" % n_clusters_)

	###############################################################################
	# Plot result
	import matplotlib.pyplot as plt
	from itertools import cycle

	plt.figure(1)
	plt.clf()

	colors = cycle('brgrcmykbgrcmykbgrcmykbgrcmyk')
	for k, col in zip(range(n_clusters_), colors):
	    my_members = labels == k
	    cluster_center = cluster_centers[k]
	    plt.plot(X[my_members, 0], X[my_members, 1], col + '.' ,markerfacecolor= 'none')
	    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor= col,
	             markeredgecolor='k', markersize=14)
	plt.xlabel(column_names[0])
	plt.ylabel(column_names[1])
	plt.title('%s   Estimated number of clusters: %d' % (in_filename, n_clusters_))
	plt.show()


datafile = "date_2005-03-01.csv"
list_of_variable =  range(4,38)

#first_arg = datafile
#second_arg = list_of_variable

if __name__ == "__main__":
	 #mean_shiftf_clustering(datafile,list_of_variable)
     mean_shiftf_clustering(datafile,list_of_variable)
