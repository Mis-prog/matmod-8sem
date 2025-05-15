import numpy as np
import matplotlib.pyplot as plt

eps = 300
y = np.linspace(0, 1, 100)
fi = y * (1 - y) * (0.5 - y) ** 2
plt.plot(y, 1 + eps * fi)
plt.show()
