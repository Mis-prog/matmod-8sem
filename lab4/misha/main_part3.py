import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def blasius_eq(eta, y):
    f, f_prime, f_double_prime = y
    f_triple_prime = - (f * f_double_prime) / 2  # Исходное уравнение
    return [f_prime, f_double_prime, f_triple_prime]

def shoot(fpp0_guess, eta_max=10, n_points=100):
    eta_vals = np.linspace(0, eta_max, n_points)
    y0 = [0, 0, fpp0_guess]  # Начальные условия: f(0)=0, f'(0)=0, f''(0)=предположение
    sol = solve_ivp(blasius_eq, [0, eta_max], y0, t_eval=eta_vals, method='RK45')
    return sol.t, sol.y

def find_optimal_fpp0(target_f_prime_inf=1, tol=1e-5, eta_max=10, n_points=100):
    fpp0_low, fpp0_high = 0.1, 1.0  # Начальный диапазон для f''(0)
    while fpp0_high - fpp0_low > tol:
        fpp0_guess = (fpp0_low + fpp0_high) / 2
        eta_vals, (f_vals, f_prime_vals, _) = shoot(fpp0_guess, eta_max, n_points)
        
        if f_prime_vals[-1] < target_f_prime_inf:
            fpp0_low = fpp0_guess  # Недооценили f''(0), надо больше
        else:
            fpp0_high = fpp0_guess  # Переоценили, надо меньше
    
    return (fpp0_low + fpp0_high) / 2

fpp0_opt = find_optimal_fpp0() 
eta_vals, (f_vals, f_prime_vals, f_double_prime_vals) = shoot(fpp0_opt)

print()

# nu = 0.53e-3 / 725     
# U_inf = 2

# Nx, Ny = 20000, 5000
# x_vals = np.linspace(0 , 2, Nx)  
# y_vals = []

# fou, Ly = 10, 1
# for j in range(Ny):
#     y_vals.append((fou ** (j * Ly / Ny  - Ly) )/ (fou - 1))
# y_vals = np.array(y_vals)

# X, Y = np.meshgrid(x_vals, y_vals)
# ETA = Y * np.sqrt(U_inf /(nu * X + 1e-9))

# for layer in ETA:
#     y0 = [0, 0, fpp0_opt]
#     sol = solve_ivp(blasius_eq,(min(layer),max(layer)),y0,t_eval=sorted(layer), method='RK45')