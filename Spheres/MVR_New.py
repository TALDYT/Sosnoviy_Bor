import bpy
import os
import numpy as np
import time
import mathutils
from numpy import exp
from bpy import context

# Версия от 01 от 02 ноября 2023
# Программа расчета освещенности и силы эммиссии
# В настоящем виде программа использует сцену состоящую из плоскости, источника света и камеры
# luminosity - освещенность
# Strength - сила эммиссии
# Перед  выполнением программы нужно настроить экран, для чего нужно выполнить следующее
# 1. Создать плоскость в плоскости XY с координатами центра (0,0,0) на экране "3DView"
# 2. Увеличить площадь квадрата, чтобы проекция от источника попадала на созданный квадрат
# 3. Перейти в режим "prerender" (необязательно)
# 4. Нажать клавишу "0", чтобы перейти на "Вид из Камеры"
# 5. Выключить "Освещение мира", перейдя на вкладку "World properties"

#-------------------------------------------------------------------------------------------
# Функция №1. В данной функции по трехмерным координатам интересующей нас точки вычисляются 
# двухмерные координаты этой точки в 2D отрендеренном изображении. Также вычисляются 
# переменные region и rv3d
def view3d_find1(coord):
    for area in context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    region, rv3d
                    from bpy_extras import view3d_utils 
                    point_pos_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, coord)
    return point_pos_2d, region, rv3d
    return None
#-------------------------------------------------------------------------------------------
# Функция №2. Данная функция создана для удобства работы Функции №3 и представляет из себя 
# обрезанный вариант Функции №1, который создан для повторного получения значений переменных
# region и rv3d 
def view3d_find2():
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    return region, rv3d
    return None, None
#--------------------------------------------------------------------------------------------
# Функция №3. Данная функция определяет координаты 2d прямоугольника видимости объектива камеры.
# Иными словами данная функция определяет поле видимости камеры
def view3d_camera_border(scene):
    obj = scene.camera
    cam = obj.data
    frame = cam.view_frame(scene=scene)
    frame = [obj.matrix_world @ v for v in frame]
    from bpy_extras.view3d_utils import location_3d_to_region_2d
    region, rv3d = view3d_find2()
    frame_px = [location_3d_to_region_2d(region, rv3d, v) for v in frame]
    return frame_px
#---------------------------------------------------------------------------------------------
# Функция №4. Эта функция пересчитывает координаты 2d  изображения на экране "3D View"  
# в координаты редактора изображений, где хранится отрендеренное изображение. В этой функции 
# используется матрица Luminocity, которая вычисляется в Функции №5. По вычисленным координатам  
# X и Y и матрице Luminocity вычисляется значение освещенности в точке с координатами X и Y.
def coordinates_2d_luminocity(coord):
    point_pos_2d, region, rv3d = view3d_find1(coord) # 2D координаты точки по размеру 3D экрана, а не растра камеры
    print("point_pos_2d", point_pos_2d)
    X = 1080 * (point_pos_2d[0] - X_min)/width  # @@@ 1920 @@@ номер пикселя точки, где определяется освещенность, по оси абцисс растра камеры
    Y = 1080 * (point_pos_2d[1] - Y_min)/height # номер пикселя точки, где определяется освещенность, по оси ординат растра камеры
    print("luminocity_X_Y_wsp =",Luminocity[int(Y),int(X)])
    luminocity_X_Y_wsp = Luminocity[int(Y),int(X)]
    return X,Y,luminocity_X_Y_wsp
#---------------------------------------------------------------------------------------------

def luminocity():
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links
    for n in tree.nodes:
        tree.nodes.remove(n)
    rl = tree.nodes.new('CompositorNodeRLayers'); rl.location = 185,285
    v = tree.nodes.new('CompositorNodeViewer'); v.location = 750,210; v.use_alpha = False
    links.new(rl.outputs[0], v.inputs[0])  # link Image output to Viewer input
    bpy.ops.render.render()
    pixels = bpy.data.images['Viewer Node'].pixels; #print(len(pixels)) # size is always width * height * 4 (rgba); # copy buffer to numpy array for faster manipulation
    arr = np.array(pixels[:])
    n_pixcel = int(len(arr)/4) #получается 2073600
    arr2 = arr.reshape(n_pixcel,4)
    type(arr2) #where channel is 0 for red, 1 for green, 2 for blue and 3 for transparency.
    R = arr2[0:n_pixcel,0]
    G = arr2[0:n_pixcel,1]
    B = arr2[0:n_pixcel,2]
    Luminocity = 0.2126 * R + 0.7152 * G + 0.0722 * B; #print(len(Luminocity))
    Luminocity = Luminocity.reshape(1080,1080)
    return Luminocity
#--------------------------------Начало программы---------------------------------
# Загрузка исходных данных
#points = np.loadtxt('C:/Blender/Visibility Matrix/coordinates.txt', delimiter=" ")
points = np.loadtxt('C:/Blender/Visibility Matrix 1000/coordinates seldom.txt', delimiter=" ")
# Удаляем старые лампы и сферы (если остались)
for ob in bpy.context.scene.objects:
    if ob.name.startswith('Point') or ob.name.startswith('Sphere'):
        bpy.data.objects.remove(ob, do_unlink=True)

scene = bpy.context.scene
mat = np.zeros((len(points), len(points)), dtype=np.int32) # Проверка видимости

for i in range(len(points)-1):
    #создаем лампу
    bpy.ops.object.light_add(type='POINT', location = points[i])
    new_light = bpy.context.active_object.data
    new_light.energy = 300000
    for j in range(i+1,len(points)):
        # Создаем сферы
        sphere_mesh = bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, enter_editmode=False, align='WORLD', location=points[j])
        sphere_object = bpy.context.active_object
    
    Luminocity = luminocity() #вид 2D. Рендерим кадр
    frame_px = view3d_camera_border(bpy.context.scene)
    print("Camera frame:", frame_px) 
    X1Y1 = frame_px[0]; X2Y2 = frame_px[1]; X3Y3 = frame_px[2]; X4Y4 = frame_px[3]
    #print("X1Y1",X1Y1); print("X2Y2",X2Y2); print("X3Y3",X3Y3); print("X4Y4",X4Y4)
    X1 =X1Y1[0]; Y1 =X1Y1[1]; X2 =X2Y2[0]; Y2 =X2Y2[1]; X3 =X3Y3[0]; Y3 =X3Y3[1]; X4 =X4Y4[0]; Y4 =X4Y4[1]
    X_min = X3; Y_min = Y3; width = X1 - X3; height = Y1 - Y3
    #---------------------------------------------------------------------------------------
    # Определение списка сфер
    spheres = [obj for obj in bpy.data.objects if obj.name.startswith("Sphere")]

    # Цикл по каждой сфере
    for index, sphere in enumerate(spheres):
        bpy.context.view_layer.objects.active = sphere
        coord = sphere.location
        print(f"Сделана активной сфера '{sphere}', координаты: {coord}")   
        X, Y, luminocity_X_Y = coordinates_2d_luminocity(coord)
        print("X =",X); print("Y =",Y); 
        print("luminocity_X_Y =",Luminocity[int(Y),int(X)])
        luminocity_X_Y= Luminocity[int(Y),int(X)]

        distance = np.linalg.norm(points[i] - sphere.location) # Расстояние между источником света и сферой

        # Критерий видимости
        threshold = 0.05  # Уровень освещённости для принятия решения
        max_distance = 15 # Наибольшая дистанция видимости
        if (luminocity_X_Y > threshold) & (distance < max_distance):
            mat[i, index+i+1] = 1  # Хорошая видимость
            mat[index+i+1, i] = 1
        else:
            mat[i, index+i+1] = 0  # Нет видимости
            mat[index+i+1, i] = 0

    # Удаляем временные объекты
    for ob in bpy.context.scene.objects:
        if ob.name.startswith('Point') or ob.name.startswith('Sphere'):
            bpy.data.objects.remove(ob, do_unlink=True) 

mat = mat + np.eye(len(points))
print("матрица mat", mat)
np.savetxt('C:/Blender/Visibility Matrix 1000/visibility seldom.txt', mat, delimiter=" ", fmt="%d")
