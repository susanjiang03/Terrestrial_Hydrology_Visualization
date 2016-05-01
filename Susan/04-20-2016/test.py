from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as n
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines
# you can also have 'l' for low, then 'h' for high. Unless coastlines are
# really important to you, or lakes, you should just use c for crude.
# m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,\
#             llcrnrlon=-180,urcrnrlon=180,resolution='c')

# m.drawcoastlines()

# #m.drawcountries()
# #m.drawstates()
# #m.drawrivers()

# #m.fillcontinents(color='#04BAE3',lake_color='#FFFFFF')
# # draw parallels and meridians.

# #m.drawparallels(np.arange(-90.,91.,30.))
# #m.drawmeridians(np.arange(-180.,181.,60.))

# m.drawmapboundary(fill_color='#FFFFFF')

# m.bluemarble()

# plt.title("Geo Plotting Tutorial")
# plt.show()

m = Basemap(projection='mill',llcrnrlat=-60,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')

m.drawcountries()
m.drawstates()

m.bluemarble()

plt.title("Geo Plotting Tutorial")
plt.show()
