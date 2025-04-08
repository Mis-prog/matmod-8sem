import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# data_c = np.loadtxt('result/regional.txt', delimiter=' ')
# data_py = np.loadtxt('result/first_values.csv', delimiter=',', skiprows=1)
# plt.figure(figsize=(12, 6))
#
# # Первый график (левая панель)
# plt.subplot(1, 2, 1)  # 1 строка, 2 столбца, первый график
# plt.plot(np.linspace(0, 2, len(data_c[:, 0])), data_c[:, 0] - data_py[:, 0][:-1])
# plt.title('Погрешность по оси X')
# plt.xlabel('X')
# plt.ylabel('Разница')
#
# # Второй график (правая панель)
# plt.subplot(1, 2, 2)  # 1 строка, 2 столбца, второй график
# plt.plot(np.linspace(0, 1, len(data_c[:, 0])), data_c[:, 1] - data_py[:, 1][:-1])
# plt.title('Погрешность по оси Y')
# plt.xlabel('X')
# plt.ylabel('Разница')
#
# # Показать оба графика
# plt.tight_layout()  # Обеспечивает правильное распределение графиков
# plt.show()


# u_c = np.loadtxt("result/results_u.txt")
v_c = np.loadtxt("result/results_v.txt")[:, 4000:]


# u_py = np.load("result/U_field.npy")
v_py = np.load("result/V_field.npy")[:, 4000:]

print(v_py)

diff = v_c - v_py

# Получаем размерности
ny, nx = diff.shape
x = np.linspace(0, 2, nx)
y = np.linspace(0, 1, ny)
X, Y = np.meshgrid(x, y)

# Строим 3D график
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, diff, cmap='seismic')

ax.set_title("Поверхность разности v_c - v_py")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Difference")

plt.show()
