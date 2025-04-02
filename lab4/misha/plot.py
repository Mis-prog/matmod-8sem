import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

filename = 'result/results.txt'

data = np.loadtxt(filename)

x = np.linspace(0, 10, data.shape[1])
y = np.linspace(0, 1, data.shape[0])
X, Y = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, data)
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
