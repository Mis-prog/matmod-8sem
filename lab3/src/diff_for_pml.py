import numpy as np
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('TkAgg')


def draw_surface(x, y, Z):
    X, Y = np.meshgrid(data_pml['x'][:1001], data_pml['y'])
    fig = plt.figure(figsize=(12, 8))  # Размер окна
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='plasma')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.show()


iter = 0
data_pml = {
    'z': np.loadtxt(f'../result_my/z_{iter}.txt'),
    'x': np.loadtxt(f'../result_my/x_{iter}.txt'),
    'y': np.loadtxt(f'../result_my/y_{iter}.txt')
}

iter = 1
data_not_pml = {
    'z': np.loadtxt(f'../result_my/z_{iter}.txt'),
    'x': np.loadtxt(f'../result_my/x_{iter}.txt'),
    'y': np.loadtxt(f'../result_my/y_{iter}.txt')
}

sum_pml = 0
for j in range(len(data_pml['z'][:, :1001])):
    for i in range(1001):
        sum_pml += data_pml['z'][j, i] * data_pml['z'][j][i]

norm_pml = np.sqrt(sum_pml)

sum_not_pml = 0
for j in range(len(data_pml['z'][:, :1001])):
    for i in range(1001):
        sum_not_pml += data_not_pml['z'][j, i] * data_not_pml['z'][j][i]

norm_not_pml = np.sqrt(sum_not_pml)

print(f'norm_pml: {norm_pml}')
print(f'norm_not_pml: {norm_not_pml}')

# draw_surface(data_pml['x'][:1001], data_pml['y'], data_pml['z'][:, :1001] / norm_pml)
# draw_surface(data_not_pml['x'][:1001], data_not_pml['y'], data_not_pml['z'][:, :1001] / norm_not_pml)
# draw_surface(data_not_pml['x'][:1001], data_not_pml['y'],
#              - data_pml['z'][:, :1001] / norm_pml + data_not_pml['z'][:, :1001] / norm_not_pml)


fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
for i in range(len(data_not_pml['y'])):
    axs[0].set_title('Разница')
    axs[0].plot(data_not_pml['x'][:1001],
                - data_pml['z'][i, :1001] / norm_pml + data_not_pml['z'][i, :1001] / norm_not_pml, color='blue')

for i in range(len(data_not_pml['y'])):
    axs[1].set_title('C PML')
    axs[1].set_ylim([-0.005,0.02])
    axs[1].plot(data_not_pml['x'][:1001],
                data_pml['z'][i, :1001]/norm_pml, color='blue')

for i in range(len(data_not_pml['y'])):
    axs[2].set_title('Без PML')
    axs[2].set_ylim([-0.005,0.02])
    axs[2].plot(data_not_pml['x'][:1001],
                data_not_pml['z'][i, :1001]/norm_not_pml, color='blue')

plt.show()


diff = data_not_pml['z'][:, :1001] / norm_not_pml - data_pml['z'][:, :1001] / norm_pml
mse = np.mean(diff**2)
print(f'MSE между с PML и без PML: {mse}')