import numpy as np 
import matplotlib.pyplot as plt 

data = np.load('lab2.npz')
ACTIVE = data['active']
COUNT = data['count']

plt.plot(COUNT,ACTIVE)
plt.xlabel('Такт')
plt.ylabel('Кол-во живых')
plt.grid()
plt.show()


# print(ACTIVE[-50:])