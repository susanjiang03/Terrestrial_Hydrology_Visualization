import math
import os
import errno
import csv
import datetime
import json
from random import shuffle
from FilterData import *
from  GetData import *


CURRENT_DIR = os.getcwd()
raw_dataFile = "indicators.csv"
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResult_DIR = PARENT_DIR + "/MeanShiftResult"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"
GRID_INDEXLIST_JSON = "grid_indexList.json"
INDEX_LATLON_JSON = "index_LatLon.json"
DATE_LIST_TXT = "date_list.txt"
LIST_OF_ALL_DATA = get_date_list() 

HEADER = ['index', 'start_date', 'lat', 'lon', 'ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans', 
'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
'energy_sw_up_-3', 'energy_sw_up_-2', 'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
'energy_sw_dn_-3', 'energy_sw_dn_-2', 'energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
'energy_lw_dn_-3', 'energy_lw_dn_-2', 'energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2']

'''
populate date_list.txt file, a list of distinct date
save in CUERRENT_DIR
'''
def populate_date_list_txt_file():
    date_list = []
    with open(raw_dataFile, 'rb') as in_f:
    	 datareader = csv.reader(in_f)
    	 #skip the headers
    	 data_as_list = list(data_as_list)[1:]
    	 for row in data_as_list:
    	 	 date = row[1]
    	 	 if date not in date_list:
    	 	 	print "find a distinct date : %s"%date
    	 	 	date_list.append(date)
    in_f.close()
    date_list.sort()
    string_date_list = " ".join(date_list)
    out_f = open(DATE_LIST_TXT,'w')
    print "Writing to date_list.txt: \n%r"%string_date_list
    out_f.write(string_date_list)
    out_f.close()

'''
write data_as_list to csv file
@data_as_list: a matrix of data
@out_fileName: dir + fileName

'''
def populate_data_as_list_to_csv_file(data_as_list,out_fileName):
	dest = out_fileName[ : out_fileName.rfind("/")]
	try:
		os.makedirs(dest)
		print "Make Dir : %s" %dest
	except OSError as exc:
		if exc.errno != errno.EEXIST:
			raise
		else:
			pass
	print '\nWriting data to %s' %out_fileName
	with open(out_fileName, 'w+') as out_f:
		writer = csv.writer(out_f)
		for row in data_as_list:
			writer.writerow(row)
	out_f.close()
	print '\nFinished writing data to %s' %out_fileName     

'''
get list of date from 'date_list.txt'
filter by date and populate csv files by date from raw data file
populate date csv file  eg. "1978-12-01.csv"
save to dir ./DateCSV/
'''	

def populate_all_date_csv_files(in_fileName,dest):
	try:
		os.makedirs(dest)
	except OSError as exc: # Guard against race condition
		if exc.errno != errno.EEXIST:
			raise
	else:
		pass
	header = get_header(in_fileName)
	date_list = get_date_list()
	for date in date_list:
		data_as_list = []
		data_as_list.append(header)
		data_as_list.extend(filter_by_date(in_fileName, date))
		out_fileName = '%s/%s.csv'%(dest, date)
		populate_data_as_list_to_csv_file(data_as_list,out_fileName)

'''
in_fileName is raw_File , or DataCSV_DIR + '/2005-12-01.csv'
populate two json files:
'grid_indexList.json' , eg. { (lat,lon) : [0, 1, 2, 3] }
'index_LatLon.json'   eg. {'0':[lat,lon]}
'''
def populate_location_json(in_fileName):

	dict_grid_indexList = {}
	dict_index_LatLon = {}
	with open(in_fileName, 'rb') as in_f:
		datareader = csv.reader(in_f)
		next(datareader, None) #skip the headers
		for line in datareader:
			index = int(line[0])
			lat = line[2]
			lon = line[3]
			lat_lon = [lat,lon]
			#index already exist in dict
			if  index in dict_index_LatLon.keys():
				continue
			else:
				dict_index_LatLon[index] = lat_lon
				print "Create new key, value in  dict_index_LatLon:  '%d' : (%r, %r)\n" %(index,lat,lon)

            #append to dict_grid_indexList
			#round to neasrest 10
			LAT = int(float(lat)/10)*10
			LON = int(float(lon)/10)*10
			LAT_LON = '(%d,%d)'%(LAT,LON)
			#dict key will be a tp of (LAT,LON), lat,lon is round to 10, floor
			#value will be a list of locations that lat in (LAT, LAT + 10), lon in (LON, LON + 10)
			if LAT_LON in dict_grid_indexList.keys():
				dict_grid_indexList[LAT_LON].append(index)
				print 'Append to dict_girdIndex[(%r,%r)''].append(%d)\n'%(LAT,LON,index)
			else:
				dict_grid_indexList[LAT_LON] = [index]
				print 'Create new key, value  in dict_girdIndex[%d]=[[%d,%d]]\n'%(index,LAT,LON)
	in_f.close()
	#print dict_locationIndex
	with open(GRID_INDEXLIST_JSON ,'w') as out_f:
		 json.dump(dict_grid_indexList, out_f)
	out_f.close()
	print "Save to dict_girdIndex %s"%GRID_INDEXLIST_JSON

	with open(INDEX_LATLON_JSON,'w') as out_f:
		 json.dump(dict_index_LatLon, out_f)
	out_f.close()
	print "Save to dict_index_LatLon%s"%INDEX_LATLON_JSON


'''
@percentage : percentage of date to populate, real number in (0,1)
populate evenly in each grid in map
run this every time will generate different samples 
write txt to PARENT_DIR/sampleLocationsTXT/%r/%r_sample_%d.txt%(percentage,num) num is the num of sample
return sample number, and a list sample locations index for this percentage
'''
def populate_sample_locations_txt(percentage):
    
	dict_grid_indexList = {}
	json_data = open(GRID_INDEXLIST_JSON,'r')
	dict_grid_indexList = json.load(json_data)
	json_data.close()

	#write only location index  to txt file, increment the number : percentage_sample_1, sample_2 , ...
	dest = '%s/P%r'%(SampleLocationsTXT_DIR,percentage) 
	try:
	   os.makedirs(dest)
	except OSError as exc: # Guard against race condition
	    if exc.errno != errno.EEXIST:
	        raise
	    else:
	    	pass

	sample_fileName_format = "P%r_Nn.txt"%(percentage)
	newSample_fileName = ""
	if os.listdir(dest) == []: 
		newSample_fileName = sample_fileName_format.replace("n","1")
	else:
		list_sample_number = []
		for fileName in os.listdir(dest):
			#sample_number is after 'N' ,before .txt
			sample_number = int(fileName[fileName.rfind('N') + 1 : fileName.rfind('.')])
			list_sample_number.append(sample_number)
		newSample_number = max(list_sample_number) + 1
		newSample_fileName = sample_fileName_format.replace("n",str(newSample_number))

	out_txt_file = os.path.join(dest,newSample_fileName)
	out_txt = open(out_txt_file,'w+')
	#value is a list of index for locations
	sampleNum = None
	list_sampleIndex = []
	for key,value in dict_grid_indexList.iteritems():
		    #total number of index location in same grid
	    num = len(value)
	    shuffle(value)     #shuffle to get first random numbers of index 
	    sampleNum = int(math.ceil(num * percentage))
	    sampleIndex = value[:sampleNum]
	    list_sampleIndex.extend(sampleIndex)

	string_list_sampleIndex = map(str, list_sampleIndex)
	out_string = " ".join(string_list_sampleIndex)
	out_txt.write(out_string)
	print "Populate new list of sample locations to:\n %s"%out_txt_file
	out_txt.close()
	return sampleNum,list_sampleIndex


'''
run after the sample list is populated in directory 
populate sample csv files for all dates 
if sample txt has not been populated yet , populate a new one 
@percentage is percentage of data
@sampleNum is sample number
@list_of_date:  the date to filter
'''
def populate_sample_date_csv_file(percentage,sampleNum, list_of_date):

    sample_fileName = SampleLocationsTXT_DIR + "/P%r/P%r_N%d.txt"%(percentage,percentage,sampleNum) 
    if not os.path.isfile(sample_fileName):
       	sampleNum, sample_indexList = populate_sample_locations_txt(percentage)
    else:
    	sample_indexList = get_sample_locations_list(percentage,sampleNum)
	#save files to :
	# dest = '%s/P%r_N%d'%(SampleCSV_DIR, percentage, sampleNum)
	# try:
	#    os.makedirs(dest)
	# except OSError as exc:
	# 	if exc.errno != errno.EEXIST:
	# 	    raise
	# 	else:
	# 		pass
    #get selected sample rows for each file in the dir,
    #save to data_as_list
    #populate csc file
	for fileName in os.listdir(DateCSV_DIR):
		if ".csv" in fileName and fileName.split(".")[0] in list_of_date:
			start = datetime.datetime.now()
			#out_fileName = '%s/P%r_N%d/P%r_N%d_%s'%(SampleCSV_DIR, percentage,sampleNum, percentage,sampleNum,fileName)

			data_as_list = []
			with open(os.path.join(DateCSV_DIR,fileName) ,'rU') as in_f:  
				reader = csv.reader(in_f)
				data_as_list = list(reader) 
				header = data_as_list[0]
				# out_f = open(out_fileName, 'w+')
				out_f = open(os.path.join(SampleCSV_DIR, fileName),'w+')
				writer = csv.writer(out_f)

				print "Start filtering data for %s"%fileName
				for row in data_as_list[1:]:
					if int(row[0]) in sample_indexList:
						writer.writerow(row)
				out_f.close()
				#print "Finished.Save to :\n  %s"%out_fileName
				end = datetime.datetime.now()
				elapsedTime = end - start
				print "Finished populate_sample_all_date_csv_files elapsedTime : " + str(elapsedTime)
			in_f.close()


'''
@the dir, where the csv  files in
@date, date in the datelist

will populate histogram counts of all 
'''

def populate_histogram_count_to_csv_file():
	date_list = get_date_list()
	for date in date_list[ date_list.index('1991-12-01') : ] :
		in_fileName = '%s/%s.csv'%(SampleCSV_DIR, date)
		data_as_list = get_data_as_list(in_fileName, range(0,39))
		list_of_labels = [ int(row[-1]) for row in data_as_list]
		n_cluster_ = max(list_of_labels) + 1
		for n in range(0,n_cluster_):
			filter_data_as_list = [row[:-1] for row in data_as_list if int(row[-1]) == n]
			for i in range(0,34):
				header = ['Days']
				data = [[int(row[i + 4])] for row in filter_data_as_list]
				out_data_as_list = []
				out_data_as_list.append(header)
				out_data_as_list.extend(data)
				out_file = '%s/Histogram/%s-%d-%d.csv'%(MeanShiftResult_DIR,date,n,i)
				populate_data_as_list_to_csv_file(out_data_as_list, out_file)
# # 	date_list = get_date_list()
# 	list_of_date = date_list[ date_list.index('1991-12-01') :]
# 	# populate_sample_date_csv_file(0.1, 1, list_of_date)
# 	for date in date_list:
# 		for fileName in os.listdir(SampleCSV_DIR):
# 			if date in fileName:
# 				in_fileName = os.path.join(SampleCSV_DIR, fileName)
# 				data_as_list = get_data_as_list(in_fileName, range(0,38))
# 				out_data_as_list = []
# 				out_data_as_list.append(HEADER[0:38])
# 				out_data_as_list.extend(data_as_list)
# 				populate_data_as_list_to_csv_file(out_data_as_list, in_fileName)


	


if __name__ == "__main__":
	in_fileName = SampleCSV_DIR + "/1991-12-01.CSV"
	header = ['name']
	header.extend(HEADER[4:38])
	out_data_as_list = [header]
	# out_data_as_list.append(header)
	list1 = [38]
	list1.extend(range(4,38))
	data_as_list = get_data_as_list(in_fileName, list1)
	# out_data_as_list.extend(data_as_list)
	filter_data_as_list = [row for row in data_as_list if int(row[0]) == 0 ]
	out_data_as_list.extend(filter_data_as_list)
	populate_data_as_list_to_csv_file(out_data_as_list, "paraller.csv")
	# # populate_histogram_count_to_csv_file()
	# header =['name','economy (mpg)','cylinders','displacement (cc)','power (hp)','weight (lb)','0-60 mph (s)','year']
	# num = len(header)
	# in_fileName = SampleCSV_DIR + "/1991-12-01.csv"
	# data_as_list = get_data_as_list(in_fileName, [])
	# for n in range(0, num):

	# for fileName in os.listdir(SampleCSV_DIR):
	# 	if fileName.endswith(".csv"):
	# 		in_fileName = os.path.join(SampleCSV_DIR, fileName)
	# 		data_as_list = get_data_as_list(in_fileName, range(0,39))
	# 		header = get_header(in_fileName)
	# 		newHeader = []
	# 		for h in header:
	# 			if "-" in h:
	# 				print "replace -"
	# 				h = h.replace("-","minus")
	# 			if "+" in h:
	# 				print "replace +"
	# 				h = h.replace("+", "plus")
	# 			newHeader.append(h)
	# 		print newHeader
	# 		out_data_as_list = []
	# 		out_data_as_list.append(newHeader)
	# 		out_data_as_list.extend(data_as_list)
	# 		populate_data_as_list_to_csv_file(out_data_as_list,in_fileName)







