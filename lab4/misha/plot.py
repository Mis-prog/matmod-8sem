import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

filename = 'result/results.txt'

data = []
with open(filename, 'r') as f:
    for line in f:
        # Преобразуем каждую строку в список чисел
        data.append([float(x) for x in line.split()])

data = np.array(data)

# Генерация координат сетки
Nx, Ny = data.shape

# Создаем сетку координат (x, y)
x = np.linspace(0, 1, Nx)
y = np.linspace(0, 1, Ny)


X, Y = np.meshgrid(x, y)


U = data
V = np.zeros_like(U)

plt.figure(figsize=(10, 6))
step = 200
plt.quiver(X[::step, ::step], Y[::step, ::step], U[::step, ::step], V[::step, ::step], scale=10, color='blue')


plt.title('Векторное поле скорости')
plt.xlabel('Индекс по оси x')
plt.ylabel('Индекс по оси y')
plt.show()