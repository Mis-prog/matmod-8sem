import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from tqdm import tqdm


def blasius_eq(eta, y):
    f, fp, fpp = y
    fppp = -0.5 * f * fpp
    return [fp, fpp, fppp]


def shoot(fpp0_guess, eta_max=400, n_points=int(5e3)):
    eta_vals = np.linspace(0, eta_max, n_points)
    y0 = [0, 0, fpp0_guess]  # f(0)=0, f'(0)=0, f''(0)=fpp0_guess
    sol = solve_ivp(blasius_eq, [0, eta_max], y0, t_eval=eta_vals)
    return eta_vals, sol.y


def find_optimal_fpp0(target_fp_inf=1.0, tol=1e-6):
    low, high = 0.3, 0.35
    while high - low > tol:
        mid = (low + high) / 2
        eta_vals, (f, fp, fpp) = shoot(mid)
        if fp[-1] < target_fp_inf:
            low = mid
        else:
            high = mid
    return (low + high) / 2


fpp0_opt = find_optimal_fpp0()
eta_vals, (f, fp, fpp) = shoot(fpp0_opt)
print(f"f'(eta_max) = {fp[-1]}")

U = 2
mu = 0.53e-3
rho = 725
nu = mu / rho


def eta_func(y, x):
    return y * np.sqrt(U / (nu * x))


def u_velocity(eta):
    return U * np.interp(eta, eta_vals, fp)


def v_velocity(eta, x):
    f_interp = np.interp(eta, eta_vals, f)
    fp_interp = np.interp(eta, eta_vals, fp)
    return 0.5 * np.sqrt(U * nu / x) * (eta * fp_interp - f_interp)


x_vals = np.linspace(0, 2, int(2e4), dtype=np.float32)
fou, Ly, Ny = 10, 1, int(5e3)
j_vals = np.arange(Ny, dtype=np.float32)
y_vals = (fou ** (j_vals / Ny) * Ly - Ly) / (fou - 1)
X, Y = np.meshgrid(x_vals, y_vals)
X = X.astype(np.float32)
Y = Y.astype(np.float32)
U_field = np.zeros_like(X, dtype=np.float32)
V_field = np.zeros_like(X, dtype=np.float32)

X_flat = X.ravel()
Y_flat = Y.ravel()

# Векторно считаем eta
eta_flat = eta_func(Y_flat, X_flat)

# Находим индексы ближайших значений eta в eta_vals
indices = np.searchsorted(eta_vals, eta_flat, side='left')
indices = np.clip(indices, 0, len(eta_vals) - 1)

# Используем значения f и fp без интерполяции
fp_vals = fp[indices]
f_vals = f[indices]

# Вычисление u и v
U_flat = U * fp_vals
V_flat = 0.5 * np.sqrt(U * nu / (X_flat)) * (eta_flat * fp_vals - f_vals)

# Возврат в форму
U_field = U_flat.reshape(X.shape)
V_field = V_flat.reshape(X.shape)

threshold = 2
epsilon = 5e-6

mask = U_field >= (threshold - epsilon)

results = []

# y_vals = np.linspace(0, Ly, Ny)
# X, Y = np.meshgrid(x_vals, y_vals)
for j in range(U_field.shape[1]):  # Перебор всех столбцов
    column_mask = mask[:, j]  # Маска для текущего столбца
    first_row_index = np.argmax(column_mask)  # Находим индекс первого True в столбце

    if column_mask[first_row_index]:  # Если условие выполняется
        first_value = U_field[first_row_index, j]
        first_x = X[first_row_index, j]
        first_y = Y[first_row_index, j]
        results.append([first_x, first_y, first_value])
        print(f"Столбец {j}: Первое значение U ≈ 2 на позиции ({first_x}, {first_y}), U = {first_value}")

np.savetxt("result/first_values.csv", results, delimiter=",", header="x,y,U", comments="")


np.save("result/U_field.npy", U_field[::2, ::2])
np.save("result/V_field.npy", V_field[::2, ::2])

y_vals = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x_vals, y_vals)

X = X.astype(np.float32)
Y = Y.astype(np.float32)
stepX, stepY = 1, 600
plt.figure(figsize=(10, 6))
plt.quiver(X[::stepX, ::stepY], Y[::stepX, ::stepY], U_field[::stepX, ::stepY], V_field[::stepX, ::stepY], scale=100,
           color='b')
plt.ylim(0, 0.025)
plt.title("Погран слой")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)

results = np.array(results)
plt.plot(results[:, 0], results[:, 1], color='red')

plt.show()
