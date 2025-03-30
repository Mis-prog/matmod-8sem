import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = np.loadtxt('../result/result20y00.700000.txt')
y = data[:, 0]
x = data[:, 1]
values = data[:, 2]

x_unique = np.unique(x)
y_unique = np.unique(y)

X, Y = np.meshgrid(x_unique, y_unique)
Z = np.zeros_like(X)

for i in range(len(x)):
    xi = np.where(x_unique == x[i])[0][0]  # Индекс x в сетке
    yi = np.where(y_unique == y[i])[0][0]  # Индекс y в сетке
    Z[yi, xi] = values[i]

fig = plt.figure(figsize=(12, 8))  # Размер окна
ax = fig.add_subplot(111, projection='3d')

# Рисуем поверхность
surf = ax.plot_surface(X, Y, Z, cmap='seismic')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.view_init(azim=225, elev=30)

plt.show()
