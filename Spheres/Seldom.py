import bpy
import numpy as np
import mathutils

points = np.loadtxt('C:/Blender/Visibility Matrix 1000/coordinates.txt', delimiter=" ")

Neighbour = np.zeros((len(points), len(points)), dtype=np.int32) # Матрица расстояний

for i in range(len(points)-1):
    for j in range(i+1,len(points)):
        distance = np.linalg.norm(points[i] - points[j]) # Расстояние между двумя выбранными точками
        max_distance = 7 # Наибольшая дистанция соседства
        if distance < max_distance:
            Neighbour[i, j] = 1  # Считаем соседом
            Neighbour[j, i] = 1
        else:
            Neighbour[i, j] = 0  # Не считаем соседом
            Neighbour[j, i] = 0
Neighbour = Neighbour + np.eye(len(points))
print("матрица Neighbour", Neighbour)
np.savetxt('C:/Blender/Visibility Matrix 1000/seldom.txt', Neighbour, delimiter=" ", fmt="%d")
