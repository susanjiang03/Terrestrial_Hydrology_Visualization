import math
import os.path
import sys
import csv
import numpy as np
from random import shuffle
import datetime


fo = open("sampleLocations.txt")
r = fo.readline()
r = r.strip()
indexList = r.split(" ")
#print indexList
sample_indexList = map(int, indexList)
#print indexList

for fileName in os.listdir(os.getcwd()):
    if fileName.startswith("19") or fileName.startswith("200"):
    	with open(fileName, 'rb') as in_f:
	        datareader = csv.reader(in_f)
	        header = datareader.next()
	        next(datareader, None) #skip the headers
	        out_filename = "sample_%s" % fileName
	        out_f = open(out_filename,'wb')
	        writer = csv.writer(out_f)
	        writer.writerow(header)
	        print "Start filtering data for file : %s" % fileName
	        start = datetime.datetime.now()
	        for line in datareader:
	            if int(line[0]) in sample_indexList:
	                writer.writerow(line)
	                #print line 
	        end = datetime.datetime.now()
	        elapsedTime = end - start
	        print "Finished filter_by_date, elapsedTime : " + str(elapsedTime)
	        
		out_f.close()
		in_f.close()

