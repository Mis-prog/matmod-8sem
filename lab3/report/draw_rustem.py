import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import matplotlib

matplotlib.use('TkAgg')

print("Текущая рабочая директория:", os.getcwd())

iter = 0
Z = np.loadtxt(f'../result_my/z_{iter}.txt')
x = np.loadtxt(f'../result_my/x_{iter}.txt')
y = np.loadtxt(f'../result_my/y_{iter}.txt')
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(12, 8))  # Размер окна
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='plasma')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

for i in range(len(y)):
    plt.plot(x[:1000], Z[i, :1000], color='blue')

plt.xlabel('x')
plt.ylabel('z')
plt.grid(True)
plt.title('Проекция на ZY')
plt.show()

print(x[:1000])

# for i in range(Ny):
#     plt.plot(x, data[i, :], color='blue')
# # plt.plot(y, data[:, 100], color='blue')
# plt.xlabel('x')
# plt.ylabel('z')
# plt.grid(True)
# plt.title('Проекция на ZX')
# plt.show()
