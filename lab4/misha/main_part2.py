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

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.integrate import solve_ivp

# # Определяем систему уравнений
# def system(x, y):
#     f, fp, fpp, fppp = y  # y[0] = f, y[1] = f', y[2] = f'', y[3] = f'''
#     return [fp, fpp, fppp, -f * fp / 2]

# # Метод стрельбы
# def shooting(s):
#     y0 = [0, 0, s, 0]  # f(0)=0, f'(0)=0, f''(0)=s, f'''(0)=0
#     sol = solve_ivp(system, (0, 10), y0, t_eval=np.linspace(0, 10, 100))
#     return sol.t, sol.y[0], sol.y[1]  # x, f(x), f'(x)

# # Подбор s методом дихотомии
# s_min, s_max = -1, 1  # Диапазон начального условия f''(0)
# tolerance = 1e-4

# while s_max - s_min > tolerance:
#     s_mid = (s_min + s_max) / 2
#     _, _, f_prime = shooting(s_mid)
#     if f_prime[-1] > 1:
#         s_max = s_mid
#     else:
#         s_min = s_mid

# # Решаем с оптимальным s
# x, f, f_prime = shooting(s_mid)

# # Построение графика
# plt.plot(x, f, label="f(x)")
# plt.plot(x, f_prime, label="f'(x)")
# plt.axhline(1, linestyle="--", color="gray", label="f' → 1")
# plt.xlabel("x")
# plt.ylabel("f, f'")
# plt.legend()
# plt.grid()
# plt.show()
