import bpy
import numpy as np

# Удаляем старые лампы и сферы (если остались)
for ob in bpy.context.scene.objects:
    if ob.name.startswith('Sphere'):
        bpy.data.objects.remove(ob, do_unlink=True)

#coordinates = np.loadtxt('C:/Blender/Visibility Matrix 1000/coordinates.txt')
#coordinates = np.loadtxt('C:/Blender/Visibility Matrix/coordinates_Uniform.txt')
#coordinates = np.loadtxt('C:/Blender/Visibility Matrix 1000/coordinates seldom.txt')

#coordinates = np.loadtxt('C:/Blender/Visibility Matrix/dominantes.txt')
#coordinates = np.loadtxt('C:/Blender/Visibility Matrix/dominantes_Uniform.txt')
#coordinates = np.loadtxt('C:/Blender/Visibility Matrix/dominantes_Uniform_band.txt')
coordinates = np.loadtxt('C:/Blender/Visibility Matrix 1000/dominantes_seldom.txt')


# Функция для создания красного материала
def create_red_material():
    # Создаем новый материал
    red_mat = bpy.data.materials.new(name="RedSphereMaterial")
    red_mat.use_nodes = True
    
    # Используем узел Principled BSDF
    nodes = red_mat.node_tree.nodes
    links = red_mat.node_tree.links
    
    # Узел материала
    bsdf = nodes["Principled BSDF"]
    output = nodes["Material Output"]
    
    # Настройки цвета (красный)
    bsdf.inputs["Base Color"].default_value = (1, 0, 0, 1)  # RGBA
    #bsdf.inputs["Specular"].default_value = 0.5  # Блеск поверхности
    bsdf.inputs["Roughness"].default_value = 0.5  # Шероховатость
    
    # Связываем узелки
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    
    return red_mat

# Основной цикл для добавления сфер
radius = 1  # Радиус сферы
material = create_red_material()

for coord in coordinates:
    # Добавляем сферу в позицию из массива координат
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        enter_editmode=False,
        align='WORLD',
        location=(coord[0], coord[1], coord[2]),
        scale=(1, 1, 1)
    )
    
    # Назначаем красную окраску сфере
    obj = bpy.context.active_object
    obj.data.materials.append(material)