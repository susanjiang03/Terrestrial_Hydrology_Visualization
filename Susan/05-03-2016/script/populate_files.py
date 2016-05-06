import math
import os.path
import csv
import json
from random import shuffle

CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]

'''
read date files in DateCSV dir 
call after filtered date csv files
'''
def get_dateList():
    
	DateCSV_Dir = PARENT_DIR + "/DateCSV"
	dateList = []
	for file in  os.listdir(DateCSV_Dir):
		date = file.split(".")[0]
		dateList.append(date)
	dateList.sort()
	dateList = dateList[1:]
	return dateList
	#print len(dateList)
	# out_f = open("dateList.txt",'w+')
	# for date in dateList:
	# 	print date
	# 	out_f.writelines(date + " ")
	# out_f.close()


'''   
read a date csv file 
append  location index to value of same key in a dict, if in same grid, 
generate a json file, 
'''
def populate_index_to_grid_json():

	dict_locationIndex = {}
	in_filename = PARENT_DIR + "/DateCSV/2000-03-01.csv"
	with open(in_filename, 'rb') as in_f:
		datareader = csv.reader(in_f)
		next(datareader, None) #skip the headers
		for line in datareader:
			index = int(line[0])
			lat = line[2]
			lon = line[3]
			#round to neasrest 10
			LAT = int(float(lat)/10)*10
			LON = int(float(lon)/10)*10
			key = '%d,%d'%(LAT,LON)
			#dict key will be a tp of (LAT,LON), lat,lon is round to 10, floor
			#value will be a list of locations that lat in (LAT, LAT + 10), lon in (LON, LON + 10)
			if key in dict_locationIndex.keys():
				dict_locationIndex[key].append(index)
			else:
				dict_locationIndex[key] = [index]
	in_f.close()
	#print dict_locationIndex
	out_json_filename = CURRENT_DIR + "/gridIndex.json"
	with open(out_json_filename,'w') as out_f:
		 json.dump(dict_locationIndex, out_f)
	out_f.close()
	#print dict_locationIndex
'''
@percentage : percentage of date to populate, real number in (0,1)
populate evenly in each grid in map
run this every time will generate different samples 
write list to sampleLocations.txt
'''
def populate_sample_locations_txt(percentage):

	dict_gridIndex = {}
	json_data = open(CURRENT_DIR + "/gridIndex.json",'r')
	dict_gridIndex = json.load(json_data)
	json_data.close()

	#write only location index  to txt file, increment the number : sampleLocations_1, sampleLocation_2 , ...
	sample_fileName_format = "sampleLocations"
	list_sample_number = []
	for filename in os.listdir(CURRENT_DIR):
		if sample_fileName_format in filename:
			sample_number = int(filename[-5])
			print filename
			list_sample_number.append(sample_number)

	newSample_number = max(list_sample_number) + 1
	out_txt_file = CURRENT_DIR + "/sampleLocations_%r_%d.txt"%(percentage,newSample_number)
	out_txt = open(out_txt_file,'w+')

    #value is a list of index for locations
	for key,value in dict_gridIndex.iteritems():
		    #total number of index location in same grid
		    num = len(value)
		    shuffle(value)     #shuffle to get first random numbers of index 
		    sampleNum = int(math.ceil(num * percentage))
		    list_sampleIndex = value[:sampleNum]
            #write only location index  to txt file 
		    for each in list_sampleIndex:
		    	out_txt.writelines(str(each) + " ")
	out_txt.close()

'''
read from sampleLocation* txt file, return a list of integer
run after sample txt file generated
@in_file : txt file name 
'''
def get_sample_locations_list(in_file):
	fo = open(in_file)
	r = fo.readline()
	r = r.strip()
	indexList = r.split(" ")
	#print indexList
	sample_indexList = map(int, indexList)
	return sample_indexList


def write_index_lat_lon_to_json():
	in_filename = PARENT_DIR + "/DateCSV/2000-03-01.csv"
	locationDict = {}
	with open(in_filename, 'rb') as in_f:
		reader = csv.reader(in_f)
		next(reader, None) 
		for line in reader:
			index,lat,lon = int(line[0]),line[2],line[3]
			if index not in locationDict.keys():
				locationDict[index] = [lat, lon]
				print index, locationDict[index]
			else:
				print str(index) + " already in dict kyes"
	in_f.close()
	print len(locationDict)
	#print locationDict
	with open(CURRENT_DIR + "/index_lat_lon.json", 'w') as fp:
	     json.dump(locationDict, fp)
	fp.close()

#write_index_lat_lon_to_json()

#json_file is pre-populate json file 
#return a dictionay with key is location index, and value is ['lat','lon']
def get_location_dict():
	d = {}
	json_data = open(CURRENT_DIR+ "/index_lat_lon.json",'r')
	d = json.load(json_data)
	json_data.close()
	print d
	return d
#get_location_dict()

#populate_sample_locations_txt(0.05)
