import matplotlib.pyplot as plt
import numpy as np

i = 0
data = np.loadtxt(f'../result_my/{i}_eigen_data.txt')

x = np.loadtxt(f'../result_my/{i}_eigen_X.txt')
y = np.loadtxt(f'../result_my/{i}_eigen_Y.txt')
z = np.loadtxt(f'../result_my/{i}_eigen_Z.txt')

X, Y = np.meshgrid(x, y)
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_title(
    f'N = {data[0]}, M = {data[1]}, L = {data[2]}, x_PML = {data[3]}, y_0 = {data[4]}, k_0 = {data[5]}, eps = {data[6]}',
    fontsize=9)
ax1.plot_surface(X, Y, z, cmap='plasma')

ax2 = fig.add_subplot(122)
for i in range(len(y)):
    ax2.plot(x, z[i, :], c='b')
plt.show()
