import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import matplotlib

matplotlib.use('TkAgg')

print("Текущая рабочая директория:", os.getcwd())

iter = 21
Z = np.loadtxt(f'../result_alia/z_{iter}.txt')
x = np.loadtxt(f'../result_alia/x_{iter}.txt')
y = np.loadtxt(f'../result_alia/y_{iter}.txt')
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(16, 6))

# Первый график — 3D поверхность
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
# fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10, label='z')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')
ax1.set_title('3D поверхность')

# Второй график — проекция на плоскость ZX
ax2 = fig.add_subplot(1, 2, 2)
for i in range(len(y)):
    ax2.plot(x, Z[i, :], color='green', alpha=0.8)

ax2.set_xlabel('x')
ax2.set_ylabel('z')
ax2.set_title('Проекция на ZX')
ax2.grid(True)

plt.tight_layout()
plt.show()


# for i in range(Ny):
#     plt.plot(x, data[i, :], color='blue')
# # plt.plot(y, data[:, 100], color='blue')
# plt.xlabel('x')
# plt.ylabel('z')
# plt.grid(True)
# plt.title('Проекция на ZX')
# plt.show()
