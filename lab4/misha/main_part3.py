import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from tqdm import tqdm

def blasius_eq(eta, y):
    f, fp, fpp = y
    fppp = -0.5 * f * fpp
    return [fp, fpp, fppp]

def shoot(fpp0_guess, eta_max=10, n_points=500):
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


U = 2
mu = 0.53e-3
rho = 725
nu = mu / rho

def eta_func(y, x):
    return y * np.sqrt(U / (nu * x + 1e-9))

def u_velocity(eta):
    return U * np.interp(eta, eta_vals, fp)

def v_velocity(eta, x):
    f_interp = np.interp(eta, eta_vals, f)
    fp_interp = np.interp(eta, eta_vals, fp)
    return 0.5 * np.sqrt(U * nu / x) * (eta * fp_interp - f_interp)


x_vals = np.linspace(0, 2, int(2e3))
y_vals = []
fou, Ly, Ny = 10, 1, int(5e3)
for j in range(Ny):
    y_vals.append((fou ** (j * Ly / Ny  - Ly) )/ (fou - 1))
y_vals = np.array(y_vals)

X, Y = np.meshgrid(x_vals, y_vals)
U_field = np.zeros_like(X)
V_field = np.zeros_like(X)

for i in tqdm(range(X.shape[0])):
    for j in range(X.shape[1]):
        x = X[i, j]
        y = Y[i, j]
        eta = eta_func(y, x)
        U_field[i, j] = u_velocity(eta)
        V_field[i, j] = v_velocity(eta, x)
        
stepX, stepY = 100, 10        
plt.figure(figsize=(10, 6))
plt.quiver(X[::stepX,::stepY], Y[::stepX,::stepY], U_field[::stepX,::stepY], V_field[::stepX,::stepY], scale=100)
plt.title("Поле скоростей в пограничном слое (уравнение Блазиуса)")
plt.xlabel("x (вдоль пластины)")
plt.ylabel("y (поперёк пластины)")
plt.grid(True)
plt.show()