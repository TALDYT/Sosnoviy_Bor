import bpy

# Название объекта, для которого нужно получить вершины
object_name = "Ways:highway"  # Замените на нужное вам название

# Открываем файл для записи
output_file_path = "C:/Blender/Грачев/vertex.txt"  # Замените путь на нужный вам

with open(output_file_path, 'w') as file:
    # Получаем объект по названию
    obj = bpy.data.objects.get(object_name)
    
    if obj and obj.type == 'MESH':  # Проверяем, что объект существует и является мешем
        mesh = obj.data
        
        # Проходим по вершинам меша
        for vertex in mesh.vertices:
            coords = vertex.co  # Координаты вершины
            line = f"{coords[0]} {coords[1]} {coords[2]}\n"
            file.write(line)
    else:
        print(f"Объект с названием '{object_name}' не найден или не является мешем.")
print("Вершины записаны в файл:", output_file_path)






