
import os
for fileName in os.listdir(os.getcwd()):
    if "csv" in fileName:
        new = fileName.replace("_sample", "")
        os.rename(os.path.join(os.getcwd(),fileName), os.path.join(os.getcwd(),new))


