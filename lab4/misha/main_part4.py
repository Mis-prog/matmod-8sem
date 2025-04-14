import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# data_c = np.loadtxt('result/regional.txt', delimiter=' ')
# data_py = np.loadtxt('result/first_values.csv', delimiter=',', skiprows=1)
# plt.figure(figsize=(12, 6))

# Первый график (левая панель)
# plt.subplot(1, 2, 1)  # 1 строка, 2 столбца, первый график
# plt.plot(data_c[:, 0], data_c[:, 0] - data_py[:, 0][:-1])
# plt.title('Погрешность по оси X')
# plt.xlabel('X')
# plt.ylabel('Разница')
#
# # Второй график (правая панель)
# plt.subplot(1, 2, 2)  # 1 строка, 2 столбца, второй график
# plt.plot(data_c[:, 1], data_c[:, 1] - data_py[:, 1][:-1])
# plt.title('Погрешность по оси Y')
# plt.xlabel('Y')
# plt.ylabel('Разница')
#
# # Показать оба графика
# plt.tight_layout()  # Обеспечивает правильное распределение графиков
# plt.show()

# plt.plot(data_c[:, 1],)

# print(data_c[:,0])
# plt.plot(data_c[:,0],data_c[:,1],label='c')
# plt.plot(data_py[:,0],data_py[:,1],label='py')
# plt.legend()
# plt.show()


# u_c = np.loadtxt("result/results_u.txt")
# v_c = np.loadtxt("result/results_v.txt")[:, 4000:]


# u_py = np.load("result/U_field.npy")
# v_py = np.load("result/V_field.npy")[:, 4000:]

# diff = v_c - v_py
#
# # Получаем размерности
# ny, nx = diff.shape
# x = np.linspace(0, 2, nx)
# y = np.linspace(0, 1, ny)
# X, Y = np.meshgrid(x, y)
#
# # Строим 3D график
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')
# surf = ax.plot_surface(X, Y, diff, cmap='seismic')
#
# ax.set_title("Поверхность разности v_c - v_py")
# ax.set_xlabel("X")
# ax.set_ylabel("Y")
# ax.set_zlabel("Difference")
#
# plt.show()


data_c = np.loadtxt('result/results_u.txt')
data_c_u = np.loadtxt('result/results_u.txt')
data_py = np.load('result/U_field.npy')

x_vals = []
fou, Ly, Ny, Nx, hx = 10, 1, int(5e3), int(2e4), 0.0001
for i in range(1, Nx + 1):
    x_vals.append(i * hx)
x_vals = np.array(x_vals)
y_vals = []
for j in range(0, Ny):
    y_j = (pow(fou, (j * 1.0 / Ny)) * Ly - Ly) / (fou - 1)
    y_j_left = (pow(fou, ((j - 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1)
    y_j_right = (pow(fou, ((j + 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1)
    y_vals.append(y_j)

print(len(y_vals[::2]))
print(len(data_c_u[:, :10000]))

# Извлекаем первый столбец для стрелок
data_c_u_column = data_c_u[:, 5000]  # первый столбец data_c_u
data_c_column = data_c[:, 5000]  # первый столбец data_c
print(data_c_u_column)
plt.plot(data_c_u_column,y_vals[::2], 'b-', label='data')
plt.show()

# # Приводим y_vals к нужной размерности, если требуется
# y_vals_reduced = y_vals[::2]
#
# X = np.zeros_like(y_vals_reduced)
# # Строим график
# plt.quiver(X, y_vals_reduced, data_c_u_column, data_c_column)
# plt.show()

