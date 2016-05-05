import math
import os.path
import sys
import csv
import numpy as np
from random import shuffle
import datetime


#  sample 1% location in each grid of map

in_filename = "1980-03-01.csv"
samplePercentage = 0.05

'''
eg. dict_locationIndex = {(50,100):[121015, 121016, 121192, 121193, 121194, 121195, 121375]}

means , for location index in list [121015, 121016, 121192, 121193, 121194, 121195, 121375] in origin file

its lat in [50,60) , its lon in [100,110)

'''
dict_locationIndex = {}

start = datetime.datetime.now()
with open(in_filename, 'rb') as in_f:
	datareader = csv.reader(in_f)

	next(datareader, None) #skip the headers
	n = 0 
	for line in datareader:
		n = n + 1
		i = int(line[0])
		#round to nearest 10
		lat = int(float(line[2])/10)*10
		lon = int(float(line[3])/10)*10
		tp = (lat, lon)
		if tp in dict_locationIndex.keys():
			dict_locationIndex[tp].append(i)
		else:
			dict_locationIndex[tp] = [i]
		
	list_sampleLocationIndex = []
	#define out_file 1 and out_file 2
	'''
	out_file1 =  "gridIndex.csv"
	out_f1 = open(out_file1,'wb')
	writer1 = csv.writer(out_f1)
	'''
	out_file2 = "sampleLocations_latLon.csv"
	out_f2 = open(out_file2,'wb')
	writer2 = csv.writer(out_f2)
	
    
    #write only location index  to txt file 
	out_txtFile = "sampleLocations.txt"
	out_txt = open(out_txtFile,'w+')
	for key, value in dict_locationIndex.iteritems():
		    # write to gridIndex.csv
		    num = len(value)
		    row = [key, num, value]
		    #in grindInext.csv row eg.  (lat,lon) | num | index_list  ----  (50,50)| 100 |  [1,2,3,]
		    #writer1.writerow(row)
		    #print num
		    shuffle(value)     #shuffle to get first random numbers of index 
		    sampleNum = int(num * samplePercentage)
		    if sampleNum  <= 1:
		    	l_sampleIndex = [value[0]]
		    	sampleNum = 1
		    else:
		        l_sampleIndex = value[:sampleNum]
            
            #write only location index  to txt file 
		    for each in l_sampleIndex:
		    	out_txt.writelines(str(each) + " ")
		    l = [key, sampleNum,l_sampleIndex]
		    writer2.writerow(l)
		    #print l
		    list_sampleLocationIndex.extend([l_sampleIndex])

out_txt.close()
#out_f1.close()	
out_f2.close()
in_f.close()