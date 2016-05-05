#filter_line 
import csv
import datetime

datafile = "indicators.csv"
#header = []


LON = [-180,-50]
LAT = [10,90]
#filter data on one date for all locations
def filter_northAmerica(in_filename):

    with open(in_filename, 'rb') as in_f:
        datareader = csv.reader(in_f)
        header = datareader.next()
       # print header
        #next(datareader, None) #skip the headers
        out_filename = "northAmerica.csv"
        out_f = open(out_filename,'wb')
        writer = csv.writer(out_f)
        writer.writerow(header)
        print "Start filtering data "
        start = datetime.datetime.now()
        
        for line in datareader:
            #line[2] is lat  line[3] is lon
            if float(line[2]) >= LAT[0] and float(line[2]) <= LAT[1] and float(line[3]) >= LON[0] and float(line[3]) <= LON[1] :
                writer.writerow(line)
                #print line 
        end = datetime.datetime.now()
        elapsedTime = end - start
        print "Finished filtering , elapsedTime : " + str(elapsedTime)




#filter data on one date for all locations
def filter_by_date(in_filename, date):
    with open(in_filename, 'rb') as in_f:
        datareader = csv.reader(in_f)
        header = datareader.next()
        print header
        next(datareader, None) #skip the headers
        out_filename = "date_"+date+".csv"
        out_f = open(out_filename,'wb')
        writer = csv.writer(out_f)
        writer.writerow(header)
        print "Start filtering data for date :"+date
        start = datetime.datetime.now()
        
        for line in datareader:
            if line[1] == date:
                writer.writerow(line)
                #print line 
        end = datetime.datetime.now()
        elapsedTime = end - start
        print "Finished filter_by_date, elapsedTime : " + str(elapsedTime)



filter_by_date("northAmerica.csv","2005-12-01")

#filter_northAmerica(datafile) 