import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
# u = np.loadtxt("result/results_u.txt")
# v = np.loadtxt("result/results_v.txt")
# regional = np.loadtxt("result/regional.txt")


# # # Определяем размеры сетки
# Ny, Nx = u.shape
# x = np.linspace(0, 2, Nx)
# y = np.linspace(0, 1, Ny)
# X, Y = np.meshgrid(x, y)



# # Отображение векторного поля
# plt.figure(figsize=(10, 6))
# stepX = 1
# stepY = 400
# plt.plot(regional[:,0],regional[:,1],color='r')
# plt.quiver(X[::stepX,::stepY], Y[::stepX,::stepY], u[::stepX,::stepY], v[::stepX,::stepY], scale=100, color="b")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.title("Погран слой")
# plt.ylim(0, 0.025)
# # plt.savefig("vector_field.png")
# plt.show()

# Апроксимация
from scipy.optimize import curve_fit
regional = np.loadtxt("result/regional.txt")

def funk(x, a):
    return a * np.sqrt(x)

x = regional[:,0]
y = regional[:,1]

params, _ = curve_fit(funk, x, y)
a_opt = params[0] 
plt.plot(x ,y,color='r', label = 'Погран слой')
plt.plot(x, funk(x, a_opt), color='black',ls='--', label=rf"Аппроксимация: $f(x) = {a_opt:.4f} \sqrt{{x}}$")  
plt.legend()
plt.show()


