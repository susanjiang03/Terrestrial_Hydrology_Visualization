import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans

# x = [1, 5, 1.5, 8, 1, 9]
# y = [2, 8, 1.8 , 8 , 0.6, 11]

# plt.scatter(x,y)
# plt.show()

# X = np.array([[1, 2, 3, 5, 6, 7], 
# 	[5, 8, 5, 6, 8, 11],
#     [1.5, 1.8, 6, 2.5 ,4.8, 3],
#     [8, 8, 7, 1.5, 3, 4], 
#     [1, 0.6, 3, 0, 3, 4], 
#     [9, 11, 4, 7, 8, 10],
#     [9, 7, 4, 1, 4, 7],
#     [5, 11, 4, 7, 9, 10],
#     [9, 7, 3, 11, 3, 4, 6],
#     [4, 11, 4, 8, 9, 11],
#     [9, 5, 4, 3, 4, 1],
#     [4, 13, 2, 3, 4, 7],
#     [3, 11, 1, 9, 11, 3],
#     [9, 11, 4, 2, 5, 8]])

# X = np.array([[1, 2, 3, 5, 6, 3], 
# 	[5, 8, 5, 6, 8, 3],
#     [1.5, 1.8, 6, 2.5, 4, 3],
#     [8, 8, 7, 1.5, 3, 3],
#     [9, 11, 4, 7, 8, 3],
#     [9, 7, 4, 1, 4, 3],
#     [5, 11, 4, 7, 9, 3],
#     [9, 7, 3, 11, 3, 3],
#     [4, 11, 4, 8, 9, 3],
#     [9, 5, 4, 3, 4, 3],
#     [4, 13, 2, 3, 4, 3],
#     [3, 11, 1, 9, 11, 3],
#     [9, 11, 4, 2, 5, 3]])

X = np.array([[1, 2], 
	[5, 8],
    [1.5, 1.8],
    [8, 8],
    [9, 11],
    [9, 7],
    [5, 11],
    [9, 7],
    [4, 11],
    [9, 5],
    [4, 13],
    [3, 11],
    [9, 11]])

kmeans = KMeans(n_clusters = 3)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

print(centroids)
print(labels)

colors = ["g.", "r.", "c.","b","y",'o']

for i in range(len(X)):
	print("coordinate:",X[i],"label:", labels[i])
	plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)


plt.scatter(centroids[:, 0], centroids[:, 1], marker = "x", s = 150, linewidths = 5, zorder = 10)

plt.show()