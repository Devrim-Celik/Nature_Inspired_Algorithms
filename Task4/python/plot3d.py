import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

my_data = np.load("setup.npy")

X = [0.2, 0.4, 0.6, 0.8, 1]
Y = [0.2, 0.4, 0.6, 0.8, 1]
X, Y = np.meshgrid(X, Y)
Z = my_data[:,2].reshape((5,5))

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
ax.set_xlabel('Intesification Rate')
ax.set_ylabel('Evaporation Rate')
ax.set_zlabel('Cost');
ax.set_title('Exploration of Evaporation-Intensification Surface');

plt.show()
