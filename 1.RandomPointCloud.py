"""
Create point cloud from random points.
"""
import numpy as np
import matplotlib.pyplot as plt

n = 100 # number of points
pcd = np.random.rand(n, 3)
#print(pcd)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pcd[:, 0], pcd[:, 1], pcd[:, 2])
plt.show()