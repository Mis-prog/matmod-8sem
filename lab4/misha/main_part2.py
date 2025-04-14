import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
u = np.loadtxt("result/results_u.txt")[:-1]
v = np.loadtxt("result/results_v.txt")[:-1]
regional = np.loadtxt("result/regional.txt")

print("Размерности:")
print("u:", u.shape)
print("v:", v.shape)

fou, Ly, Ny, Nx, hx = 10, 1, int(5e3), int(2e4), 0.0001
y_vals = []
for j in range(0, Ny - 1):
    y_j = (pow(fou, (j * 1.0 / Ny)) * Ly - Ly) / (fou - 1)
    y_j_left = (pow(fou, ((j - 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1)
    y_j_right = (pow(fou, ((j + 1) * 1.0 / Ny)) * Ly - Ly) / (fou - 1)
    y_vals.append(y_j)

# # Определяем размеры сетки
Ny, Nx = u.shape
x = np.linspace(0, 2, Nx)
y = np.array(y_vals[::2][:-1])
X, Y = np.meshgrid(x, y)

U_field = np.load("result/U_field.npy")
V_field = np.load("result/V_field.npy")

print("U_field:", U_field.shape)
print("V_field:", V_field.shape)
print("X:", X.shape)
print("Y:", Y.shape)

# Отображение векторного поля
plt.figure(figsize=(10, 6))
stepX = 50
stepY = 300
# plt.plot(regional[:,0],regional[:,1],color='r')
# plt.quiver(X[::stepX,::stepY], Y[::stepX,::stepY], u[::stepX,::stepY], v[::stepX,::stepY], scale=100, color="b")
# plt.quiver(X[::stepX, ::stepY], Y[::stepX, ::stepY], U_field[::stepX, ::stepY], V_field[::stepX, ::stepY], scale=100,
#            color='b')

plt.plot(U_field[:, 4900], y, color='b',label='py')
plt.plot(u[:, 5000], y, color='r',label='c')
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.ylim(0,0.005)
# plt.xlim(0.9,1.1)
plt.title("Погран слой")
# plt.ylim(0, 0.025)
# plt.savefig("vector_field.png")


plt.show()

# Апроксимация
# from scipy.optimize import curve_fit
# regional = np.loadtxt("result/regional.txt")

# def funk(x, a):
#     return a * np.sqrt(x)

# x = regional[:,0]
# y = regional[:,1]

# params, _ = curve_fit(funk, x, y)
# a_opt = params[0] 
# plt.plot(x ,y,color='r', label = 'Погран слой')
# plt.plot(x, funk(x, a_opt), color='black',ls='--', label=rf"Аппроксимация: $f(x) = {a_opt:.4f} \sqrt{{x}}$")  
# plt.legend()
# plt.show()
