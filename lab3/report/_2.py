# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import os
# import matplotlib
#
# matplotlib.use('TkAgg')
#
# print("Текущая рабочая директория:", os.getcwd())
#
# iter =100
# Z = np.loadtxt(f'../result_my/z_{iter}.txt')
# x = np.loadtxt(f'../result_my/x_{iter}.txt')
# y = np.loadtxt(f'../result_my/y_{iter}.txt')
# X, Y = np.meshgrid(x, y)
#
# # iter =34
# # _Z = np.loadtxt(f'../result_my/z_{iter}.txt')
# # _x = np.loadtxt(f'../result_my/x_{iter}.txt')
# # _y = np.loadtxt(f'../result_my/y_{iter}.txt')
# # _X, _Y = np.meshgrid(_x, _y)
#
# fig = plt.figure(figsize=(16, 6))
#
# # Первый график — 3D поверхность
# ax = fig.add_subplot(1, 1, 1, projection='3d')
# surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8)
# # fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10, label='z')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# ax.set_title('3D поверхность')
# plt.plot()
#
# # # Второй график — проекция на плоскость ZX
# # ax2 = fig.add_subplot(1, 2, 2, projection='3d')
# # # for i in range(len(y)):
# # #     ax2.plot(x, Z[i, :], color='blue', alpha=0.8)
# # #
# # # ax2.set_xlabel('x')
# # # ax2.set_ylabel('z')
# # # ax2.set_title('Проекция на ZX')
# # # ax2.grid(True)
# #
# # ax2.plot_surface(_X, _Y, _Z, cmap='plasma', alpha=0.8)
# # # fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10, label='z')
# # ax2.set_xlabel('x')
# # ax2.set_ylabel('y')
# # ax2.set_zlabel('z')
# # ax2.set_title('3D поверхность')
# #
# # plt.tight_layout()
# # plt.show()
#
#
# # for i in range(len(y)):
# #     plt.plot(_x, _Z[i, :], color='blue')
# # # plt.plot(y, data[:, 100], color='blue')
# # plt.xlabel('x')
# # plt.ylabel('z')
# # plt.grid(True)
# # plt.title('Проекция на ZX')
# # plt.show()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import matplotlib

matplotlib.use('TkAgg')

print("Текущая рабочая директория:", os.getcwd())
#eps0 1 20 ynull = 0.5 100 101 102
#eps1  ynull 0.7  200 201
#eps 20 300
iter = 202
Z = np.loadtxt(f'../result_my/z_{iter}.txt')
x = np.loadtxt(f'../result_my/x_{iter}.txt')
y = np.loadtxt(f'../result_my/y_{iter}.txt')
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(16, 6))

# Первый график — 3D поверхность
ax = fig.add_subplot(1, 1, 1, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('3D поверхность')

# Включение цветовой шкалы
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='z')

# Отображение графика
plt.show()
