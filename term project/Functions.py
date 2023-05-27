import random
def Read_file(file_name):
    # 读取文件
    with open(file_name) as f:
        lines = f.readlines()

    # 提取节点列表和邻接矩阵
    nodes = set()
    for line in lines:
        node1, node2, distance = line.strip().split()
        nodes.add(node1)
        nodes.add(node2)
        
    nodes = sorted(nodes)

    nodes[49] = nodes[0]
    nodes[0] = 'O'

    # 建立节点到索引的映射
    node_index_map = {node:index for index, node in enumerate(nodes)}

    # 初始化邻接矩阵为0
    adj_matrix = [[0 for i in range(len(nodes))] for j in range(len(nodes))]

    # 填充邻接矩阵
    for line in lines:
        node1, node2, distance = line.strip().split()
        i = node_index_map[node1]
        j = node_index_map[node2]
        adj_matrix[i][j] = float(distance)
        adj_matrix[j][i] = float(distance)

    # 输出结果
    print("节点列表：", nodes)
    return nodes,node_index_map,adj_matrix

def floyd(adj_matrix):
    n = len(adj_matrix)
    dist = [[float('inf')] * n for _ in range(n)]
    path = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] != 0 or i==j:
                dist[i][j] = adj_matrix[i][j]
                path[i][j] = i
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path[i][j] = path[k][j]
    return dist, path

def path_expansion(list, Path):
    i = 0
    while i < len(list)-1:
        extra_node = Path[list[i]][list[i+1]]
        if extra_node != list[i]:
            list.insert(i + 1, extra_node)
            i -= 1
        i += 1
    return list

def generate_random_path(team_num = 3, path_len=53, random_path = None):
    if random_path == None:
        random_path = [x for x in range(1, path_len)] 

    for i in range(team_num - 1):
        random_path.append(0)
    random.shuffle(random_path)
    random_path.insert(0,0)
    random_path.append(0)

    return random_path

def calculate_path_cost(path, dist, true_cost=False, team_num = 3, penalty = 0.4):
    
    cost = 0
    for i in range(len(path)-1):
        cost += dist[path[i]][path[i+1]]
    
    if true_cost==False:
        paths = split_path(path, team_num = team_num, expand = False)

        cost_ = cost
        max_cost = float("-inf")
        min_cost = float("inf")
        for temp_path in paths:
            temp_cost = calculate_path_cost(temp_path, dist, true_cost=True)
            max_cost = max(temp_cost, max_cost)
            min_cost = min(temp_cost, min_cost)
            # cost += 100 * max((len(temp_path)-2-(56/team_num)),0)
            # cost += 0.3 * abs(temp_cost-(cost_/team_num))
        cost += penalty*(max_cost-min_cost) #/max_cost
        # cost = max_cost
    return cost

def split_path(path, Path=None ,team_num = 3, expand = True):
    path_ = path.copy()
    del path_[len(path)-1]
    del path_[0]

    paths = []
    for i in range(team_num - 1):
        temp_path = path_[:path_.index(0)+1]
        temp_path.insert(0,0)
        path_ = path_[path_.index(0)+1:]
        if expand:
            paths.append(path_expansion(temp_path, Path))
        else:
            paths.append(temp_path)

    path_.insert(0,0)
    path_.append(0)
    if expand:
        paths.append(path_expansion(path_, Path))
    else:
        paths.append(path_)
    
    return paths

def init_time_stay (nodes,node_index_map):
    stay_time = [1 for x in range(0,len(nodes))]
    for node in nodes:
        if node.isupper():
            stay_time[node_index_map[node]] = 2
        elif node.islower():
            stay_time[node_index_map[node]] = 0
    stay_time[node_index_map["O"]] = 0
    return stay_time

def calculate_one_team_time_cost(temp_path, dist, stay_time, velocity=35):
    temp_cost = 0
    for i in range(len(temp_path)-1):
        temp_cost += dist[temp_path[i]][temp_path[i+1]]/velocity
        temp_cost += stay_time[temp_path[i]]
    return temp_cost

def calculate_time_cost(path, dist, stay_time, velocity=35, true_cost=False, team_num = 3):
    paths = split_path(path, team_num = team_num, expand = False)
    cost = 0
    for temp_path in paths:
        temp_cost = calculate_one_team_time_cost(temp_path, dist, stay_time, velocity=velocity)
        if temp_cost>cost:
            cost = temp_cost
            
    return cost

# import numpy as np
# def kmeans(dist, nodes, k):
#     # 初始化聚类中心
#     centroids = nodes[:k]

#     # 迭代直到收敛
#     while True:
#         # 初始化每个点的标签为-1，表示没有被分配到任何聚类
#         labels = np.zeros(len(nodes)) - 1

#         # 对于每个点，计算距离最近的聚类中心，并将其标签设置为该聚类中心的索引
#         for i, node1 in enumerate(nodes):
#             distances = []
#             for node2 in centroids:
#                 distances.append(dist[node1,node2])
#             labels[i] = np.argmin(distances)

#         # 计算每个聚类中心的新位置
#         new_centroids = np.zeros((k, len(nodes[0])))
#         for i in range(k):
#             points = nodes[labels == i]
#             if len(points) > 0:
#                 new_centroids[i] = np.mean(points, axis=0)

#         # 如果聚类中心没有发生变化，则停止迭代
#         if np.all(centroids == new_centroids):
#             break

#         # 更新聚类中心
#         centroids = new_centroids

#     # 返回聚类中心和每个点的标签
#     return centroids, labels