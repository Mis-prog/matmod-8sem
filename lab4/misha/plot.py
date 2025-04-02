import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
u = np.loadtxt("result/results_u.txt")
v = np.loadtxt("result/results_v.txt")


# Определяем размеры сетки
Ny, Nx = u.shape
x = np.linspace(0, 2, Nx)
y = np.linspace(0, 1, Ny)
X, Y = np.meshgrid(x, y)


# # Отображение векторного поля
plt.figure(figsize=(10, 6))
stepX = 1
stepY = 400
plt.quiver(X[::stepX,::stepY], Y[::stepX,::stepY], u[::stepX,::stepY], v[::stepX,::stepY], scale=100, color="b")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Векторное поле скорости")
plt.ylim(0, 0.025)
plt.savefig("vector_field.png")
# # plt.show()
