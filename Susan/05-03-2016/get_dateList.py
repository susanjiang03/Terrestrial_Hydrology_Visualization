'''
generate the list of date,
save in csv file
date is from "1978-12-01" to "2007-09-01"
'''

month = ["03","06","09","12"]
minYear = 1979
maxYear = 2007
#dateList = []

out_filename = "dateList.txt"
out_f = open(out_filename,'w+')
     #write first year that does not have 4 month date
out_f.writelines("1978-12-01 ")
#dateList.append("1978-12-01")
# print "1978-12-01"
yr = 1978
while yr < maxYear:
   yr = yr + 1
   for m in month:
     if yr == 2007 and m == "12":
     	break
     else:
 	 	 date = str(yr) + "-"+ m + "-01"
 	 	 #dateList.append(date)
 	 	 out_f.writelines(date + " ")
 	 	 #print date

out_f.close()



