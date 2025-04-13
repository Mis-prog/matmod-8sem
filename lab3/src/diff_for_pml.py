import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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


# fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
# for i in range(len(data_not_pml['y'])):
#     axs[0].set_title('Not PML - PML')
#     axs[0].plot(data_not_pml['x'][:1001],
#                  - data_pml['z'][i, :1001] / norm_pml + data_not_pml['z'][i, :1001] / norm_not_pml, color='blue')
#
# for i in range(len(data_not_pml['y'])):
#     axs[1].set_title('C PML')
#     axs[1].set_ylim([-0.005,0.02])
#     axs[1].plot(data_not_pml['x'][:1001],
#                 data_pml['z'][i, :1001]/norm_pml, color='blue')
#
# for i in range(len(data_not_pml['y'])):
#     axs[2].set_title('Без PML')
#     axs[2].set_ylim([-0.005,0.02])
#     axs[2].plot(data_not_pml['x'][:1001],
#                 data_not_pml['z'][i, :1001]/norm_not_pml, color='blue')
# plt.show()

# diff = data_not_pml['z'][:, :1001] / norm_not_pml - data_pml['z'][:, :1001] / norm_pml
# mse = np.mean(diff**2)
# print(f'MSE между с PML и без PML: {mse}')

x = data_not_pml['x'][:1001]
z_not_pml = data_not_pml['z'][:, :1001] / norm_not_pml
z_pml = data_pml['z'][:, :1001] / norm_pml
z_diff = -z_pml + z_not_pml

# Инициализируем фигуру
fig = go.Figure()

# Максимальная кратность
max_step = 10

# Добавим трассы для разных step (каждую n-ю линию)
for step in range(1, max_step + 1):
    visible = [False] * ((max_step) * 3)
    traces = []

    for i in range(0, len(z_not_pml), step):
        trace1 = go.Scatter(x=x, y=z_not_pml[i], mode='lines',
                            name='NOT PML' if i == 0 else None,
                            line=dict(color='blue'),
                            visible=(step == 1))
        trace2 = go.Scatter(x=x, y=z_pml[i], mode='lines',
                            name='PML' if i == 0 else None,
                            line=dict(color='green', dash='dot'),
                            visible=(step == 1))
        trace3 = go.Scatter(x=x, y=z_diff[i], mode='lines',
                            name='DIFF' if i == 0 else None,
                            line=dict(color='red', dash='dash'),
                            visible=(step == 1))
        traces.extend([trace1, trace2, trace3])

    fig.add_traces(traces)

# Слайдерные шаги
steps = []
for s, step in enumerate(range(1, max_step + 1)):
    visibility = []
    for i in range(max_step):
        # Скрываем все, кроме текущего шага
        show = (i == s)
        n_lines = len(range(0, len(z_not_pml), i + 1))
        visibility.extend([show] * (n_lines * 3))
    steps.append(dict(method="update",
                      label=f"Каждую {step}-ю",
                      args=[{"visible": visibility}]))

# Добавим слайдер
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Кратность: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders,
    title="Сравнение профилей: NOT PML, PML и DIFF",
    xaxis_title="X",
    yaxis_title="Амплитуда",
    height=600
)

fig.show()