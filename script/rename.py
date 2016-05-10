
import os

CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResult_DIR = PARENT_DIR + "/MeanShiftResult"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"


old = "_sample_"
new =  "_"
the_dir = SampleCSV_DIR + "/P0.05_N1"
for fileName in os.listdir(the_dir):
    if old in fileName:
        newName = fileName.replace(old, new)
        os.rename(os.path.join(the_dir,fileName), os.path.join(the_dir,newName))
        print "rename in %s\n%s"%(the_dir,newName) 
	# else:
	# 	print "name pattern not exits"


