import bpy
import numpy as np

def find_minimum_dominating_set(matrix_visibility):
    """
    Нахождение минимального доминирующего множества вершин с помощью жадного алгоритма.
        :param matrix_visibility: Матрица видимости, где M[i][j]=1, если вершины i и j видят друг друга.
    :return: Минимальное доминирующее множество вершин.
    """
    num_vertices = len(matrix_visibility)
    visited = set()           # Набор вершин, которые уже покрыты (просмотрены)
    dominating_set = set()    # Доминирующее множество вершин, которые покрывают все остальные
    
    # Продолжаем, пока не все вершины охвачены покрытием
    while len(visited) < num_vertices:
        max_coverage = -1       # Максимальное количество покрытых вершин (-1)
        best_vertex = None      # Вершина, обеспечивающая наилучшее покрытие
        
        # Находим вершину, которая покрывает наибольший набор непросмотренных вершин
        for v in range(num_vertices):
            if v not in visited:
                # Суммируем количество соседних непросмотренных вершин
                coverage = sum(1 for u in range(num_vertices) if matrix_visibility[v][u] == 1 and u not in visited)
                
                if coverage > max_coverage:
                    max_coverage = coverage
                    best_vertex = v
            
        # Добавляем вершину в доминирующее множество
        dominating_set.add(best_vertex)
        
        # Обновляем множество просмотренных вершин, добавив соседей выбранной вершины
        neighbors = [u for u in range(num_vertices) if matrix_visibility[best_vertex][u] == 1]
        visited.update(neighbors)
    
    return dominating_set
 
# Основной блок выполнения
if __name__ == "__main__":
    # считывание матрицы с диска
    matrix_visibility = np.loadtxt('C:/Blender/Visibility Matrix 1000/visibility seldom.txt')
    filename = 'C:/Blender/Visibility Matrix 1000/coordinates seldom.txt'
    points = np.loadtxt(filename, delimiter=' ')

    # Поиск минимального доминирующего множества
    min_dom_set = find_minimum_dominating_set(matrix_visibility)
    print("Минимальное доминирующее множество вершин:", sorted(min_dom_set))
    nomers = sorted(min_dom_set) #номера точек из доминирующего списка без учета ранга
    #вычисление ранга всех точек, которые были изначально  
    numbers = np.arange(matrix_visibility.shape[0])  # Номер точки (номер строки)
    sums = np.sum(matrix_visibility, axis=1) # Суммы элементов каждой строки матрицы
    rank = np.column_stack((numbers, sums)) # Объединяем номера и суммы в матрицу
    print('Ранг точки', rank) 
    #создание списка координат доминирующего множества пунктов мониторинга
    points = points[nomers] 
    table = np.column_stack((nomers,sums[nomers])) 
    threshold = 0
    print('порог = ',threshold)
    filtered_indices = table[:, 1] > threshold # Индексы строк, где второй столбец больше порога
    filtered_matrix = table[filtered_indices] # Фильтрованная матрица
    print(filtered_matrix)
    points = points[filtered_indices] # фильтрованный по рангу список точек
    #вывод фильтрованного по рангу списка доминирующих точек
    np.savetxt('C:/Blender/Visibility Matrix 1000/dominantes_seldom.txt', points, delimiter=" ")
    