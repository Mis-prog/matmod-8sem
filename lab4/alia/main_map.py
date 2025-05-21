import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import LogLocator, FormatStrFormatter

# Загрузка данных
stab1 = np.loadtxt("result/stab1.txt")
stab2 = np.loadtxt("result/stab2.txt")

stab1 = np.nan_to_num(stab1, nan=np.nanmax(stab1))
stab2 = np.nan_to_num(stab2, nan=np.nanmax(stab2))

Ny, Nx = stab1.shape
x = np.linspace(0, 2, Nx)
y = np.linspace(0, 1, Ny)
X, Y = np.meshgrid(x, y)

# Создание графиков
fig, axs = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

for ax, data, title in zip(
        axs,
        [stab1, stab2],
        ["Stability 1", "Stability 2"]
):
    # Логарифмическая нормализация
    vmin = np.clip(np.min(data[data > 0]), 1e-8, None)
    vmax = np.max(data)
    norm = colors.LogNorm(vmin=vmin, vmax=vmax)
    levels = np.logspace(np.log10(vmin), np.log10(vmax), 50)

    # Контурный график
    contour = ax.contourf(X, Y, data, levels=levels, cmap='plasma', norm=norm)
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label(f"{title} value")
    cbar.ax.yaxis.set_major_locator(LogLocator(base=10.0))
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))

    # Оформление
    ax.set_title(f"{title} (log scale)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)

plt.show()