
import os

# import matplotlib.pyplot as plt
# plt.hist([1, 2, 1], bins=[0, 1, 2, 3])
# #(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
# plt.show()

CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResult_DIR = PARENT_DIR + "/MeanShiftResult"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"


old = "archive"
new =  "SampleCSVarchive"
the_dir = PARENT_DIR
print PARENT_DIR
for fileName in os.listdir(the_dir):
    if fileName.startswith(old):
        newName = fileName.replace(old, new)
        os.rename(os.path.join(the_dir,fileName), os.path.join(the_dir,newName))
        print "rename in %s\n%s"%(the_dir,newName) 
	# else:
	# 	print "name pattern not exits"


