import csv
import datetime

txtFile = "dateList.txt"
in_filename = "indicators.csv"

def filter_by_date(date):
    with open(in_filename, 'rb') as in_f:
        datareader = csv.reader(in_f)
        header = datareader.next()
        print header
        next(datareader, None) #skip the headers
        out_filename = date+".csv"
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
    out_f.close()
    in_f.close()


if __name__ == "__main__":
   fo = open(txtFile)
   r = fo.readline()
   dateList = r.split(" ")
   for date in dateList:
       filter_by_date(date)