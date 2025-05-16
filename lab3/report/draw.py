import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button
import os
import matplotlib


matplotlib.use('TkAgg')


iter1 = 1002

data1 = np.loadtxt(f'../result_alia/data_{iter1}.txt')
Z1 = np.loadtxt(f'../result_alia/z_{iter1}.txt')
x1 = np.loadtxt(f'../result_alia/x_{iter1}.txt')
y1 = np.loadtxt(f'../result_alia/y_{iter1}.txt')
X1, Y1 = np.meshgrid(x1, y1)

iter2 = 1001

data2 = np.loadtxt(f'../result_alia/data_{iter2}.txt')
Z2 = np.loadtxt(f'../result_alia/z_{iter2}.txt')
x2 = np.loadtxt(f'../result_alia/x_{iter2}.txt')
y2 = np.loadtxt(f'../result_alia/y_{iter2}.txt')
X2, Y2 = np.meshgrid(x2, y2)

fig = plt.figure(figsize=(16, 6))
ax1 = fig.add_subplot(1, 3, 1, projection='3d')

surf1 = ax1.plot_surface(X1, Y1, Z1, cmap='viridis', alpha=0.9)
ax1.set_title(f'ynull = {data1[0]}, eps = {data1[1]}, k = {data1[2]}')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')

ax2 = fig.add_subplot(1, 3, 2, projection='3d')

surf2 = ax2.plot_surface(X2, Y2, Z2, cmap='viridis', alpha=0.9)
ax2.set_title(f'ynull = {data2[0]}, eps = {data2[1]}, k = {data2[2]}')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_zlabel('z')

plt.show()