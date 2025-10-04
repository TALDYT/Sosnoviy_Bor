import bpy
import os
import numpy as np
import time

# Загрузка исходных данных
filename = 'C:/Blender/Грачев/vertex.txt'
points = np.loadtxt(filename, delimiter=' ')
points = points / 20

# Выбор подмножества точек
num_points = 1000
indices = np.random.choice(range(len(points)), num_points, replace=False)
indices = np.sort(indices)
points = points[indices]

# Сохранение координат
np.savetxt('C:/Blender/Visibility Matrix 1000/coordinates.txt', points, delimiter=" ")