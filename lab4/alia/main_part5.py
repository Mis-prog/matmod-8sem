import matplotlib.pyplot as plt
import numpy as np

data_c = np.loadtxt('result/results_u.txt')
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

y_vals = np.array(y_vals)
print(len(y_vals))
print(len(data_c[:, 5000][:-1]))
print(len(data_py[:, 5000]))

DATA_Y = y_vals[::2][:-1]
DATA_C = data_c[:, 5000][:-1]
DATA_PY = data_py[:, 5000]

plt.plot(DATA_C, DATA_Y, label = 'РС')
plt.plot(DATA_PY, DATA_Y,label='ОДУ')
plt.ylim(0,0.015)
plt.legend()
plt.grid()
plt.show()
