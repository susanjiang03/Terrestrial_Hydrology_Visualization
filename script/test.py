
import os
import matplotlib.pyplot as plt
CURRENT_DIR = os.getcwd()
PARENT_DIR = CURRENT_DIR[:CURRENT_DIR.rfind("/")]
DateCSV_DIR = PARENT_DIR + "/DateCSV"
MeanShiftResult_DIR = PARENT_DIR + "/MeanShiftResult"
SampleCSV_DIR = PARENT_DIR + "/SampleCSV"
SampleLocationsTXT_DIR = PARENT_DIR + "/SampleLocationsTXT"


# plt.hist([1, 2, 1], bins=[0, 1, 2, 3])
# #(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
# plt.show()


# plt.hist([80, 15, 40, 33, 22, 58, 66, 30, 20], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80,90])
# #(array([0, 2, 1]), array([0, 1, 2, 3]), <a list of 3 Patch objects>)
# plt.show()





# new =  ""
# the_dir = MeanShiftResult_DIR + "/HISTOGRAMS/P0.1_N1_Q0.1_[ALL]"
# print PARENT_DIR
# for fileName in os.listdir(the_dir):
# 	for i in range(4,38):
# 		if "%d_"%i in fileName:
# 			c = fileName[2:4]
# 			newName = "V%d_%s.jpg"%(i,c)
# 			#newName = fileName.replace(name, "")
# 			#print fileName
# 			os.rename(os.path.join(the_dir,fileName + ".jpg"), os.path.join(the_dir,newName))
# 			print "rename in %s\n%s"%(the_dir,newName) 
# 	# else:
# 	# 	#print "name pattern not exits"


# import numpy as np
# import pylab as P
# #
# # first create a single histogram
# #
# mu, sigma = 200, 25
# x = mu + sigma*P.randn(10000)
# #
# # finally: make a multiple-histogram of data-sets with different length
# #
# x0 = mu + sigma*P.randn(10000)
# x1 = mu + sigma*P.randn(7000)
# x2 = mu + sigma*P.randn(3000)

# # and exercise the weights option by arbitrarily giving the first half
# # of each series only half the weight of the others:

# w0 = np.ones_like(x0)
# w0[:len(x0)/2] = 0.5
# w1 = np.ones_like(x1)
# w1[:len(x1)/2] = 0.5
# w2 = np.ones_like(x2)
# w0[:len(x2)/2] = 0.5



# P.figure()

# n, bins, patches = P.hist( [x0,x1,x2], 10, weights=[w0, w1, w2], histtype='bar')

# P.show()


# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Scatter(
    x=[0, 1, 2],
    y=[10, 11, 12]
)
trace2 = go.Scatter(
    x=[2, 3, 4],
    y=[100, 110, 120],
)
trace3 = go.Scatter(
    x=[3, 4, 5],
    y=[1000, 1100, 1200],
)
fig = tools.make_subplots(rows=3, cols=1, specs=[[{}], [{}], [{}]],
                          shared_xaxes=True, shared_yaxes=True,
                          vertical_spacing=0.001)
fig.append_trace(trace1, 3, 1)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 1, 1)

fig['layout'].update(height=600, width=600, title='Stacked Subplots with Shared X-Axes')
plot_url = py.plot(fig, filename='stacked-subplots-shared-xaxes')