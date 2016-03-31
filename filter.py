#filter_line 
import csv
import datetime

datafile = "indicators.csv"

#filter data on one location by index for all dates, land-mask
def filter_by_index(in_filename, index):
    with open(in_filename, 'rb') as in_f:

        datareader = csv.reader(in_f)
        header = datareader.next()
        next(datareader, None) #skip the headers

        out_filename = "location_"+str(index)+".csv"
        out_f = open(out_filename,'wb')
        writer = csv.writer(out_f)
        writer.writerow(header)

        print "Start filtering data for location : "+str(index)
        start = datetime.datetime.now()

        for line in datareader:
            #filter line[0]
            if int(line[0]) == index:
               writer.writerow(line)

        end = datetime.datetime.now()
        elapsedTime = end - start
        print "Finished filter_by_index, elapsedTime : " + str(elapsedTime)


#filter data on one date for all locations
def filter_by_date(in_filename, date):
    with open(in_filename, 'rb') as in_f:

        datareader = csv.reader(in_f)
        header = datareader.next()
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

        end = datetime.datetime.now()
        elapsedTime = end - start
        print "Finished filter_by_date, elapsedTime : " + str(elapsedTime)



#filter_by_index(datafile, 3000)
#filter_by_date(datafile, "2005-12-01")
