import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = np.loadtxt('../result/result20y00.50.txt')
Ny, Nx = data.shape
print(Ny, Nx)
x = np.linspace(0, 15, Nx)
y = np.linspace(0, 1, Ny)
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(12, 8))  # Размер окна
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, data, cmap='plasma')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

for i in range(Nx):
    plt.plot(y, data[:, i], color='blue')
# plt.plot(y, data[:, 100], color='blue')
plt.xlabel('x')
plt.ylabel('z')
plt.grid(True)
plt.title('Проекция на ZY')
plt.show()

for i in range(Ny):
    plt.plot(x, data[i, :], color='blue')
# plt.plot(y, data[:, 100], color='blue')
plt.xlabel('x')
plt.ylabel('z')
plt.grid(True)
plt.title('Проекция на ZX')
plt.show()