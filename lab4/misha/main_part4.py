import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

u_c = pd.read_csv("result/results_u.txt", header=None,sep=' ', dtype=np.float32).values
# v_c = np.loadtxt("result/results_v.txt")

# u_py = np.loadtxt("result/U_field.txt")
# v_py = np.loadtxt("result/V_field.txt")
