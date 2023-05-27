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
    # 建立节点到索引的映射
    node_index_map = {node:index for index, node in enumerate(sorted(nodes))}

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

def Read_file_ACO(file_name,team_num):
    # 读取文件
    with open(file_name) as f:
        lines = f.readlines()

    # 提取节点列表和邻接矩阵
    nodes_ACO = set()
    for line in lines:
        node1, node2, distance = line.strip().split()
        nodes_ACO.add(node1)
        nodes_ACO.add(node2)

    nodes_ACO = sorted(nodes_ACO)
    for i in range(team_num - 1):
        nodes_ACO.append('O'+str(i+1))
    # 建立节点到索引的映射
    node_index_map_ACO = {node:index for index, node in enumerate(sorted(nodes_ACO))}
    nodes_ACO = sorted(nodes_ACO)

    # 初始化邻接矩阵为0
    adj_matrix_ACO = [[0 for i in range(len(nodes_ACO))] for j in range(len(nodes_ACO))]

    # 填充邻接矩阵
    for line in lines:
        node1, node2, distance = line.strip().split()
        i = node_index_map_ACO[node1]
        j = node_index_map_ACO[node2]
        adj_matrix_ACO[i][j] = float(distance)
        adj_matrix_ACO[j][i] = float(distance)

    for i in range(1, team_num):
        for j in range(len(nodes_ACO)):
            adj_matrix_ACO[node_index_map_ACO['O'+str(i)]][j] = adj_matrix_ACO[node_index_map_ACO['O']][j]
            adj_matrix_ACO[j][node_index_map_ACO['O'+str(i)]] = adj_matrix_ACO[j][node_index_map_ACO['O']]
        adj_matrix_ACO[node_index_map_ACO['O'+str(i)]][node_index_map_ACO['O']] = 0
        adj_matrix_ACO[node_index_map_ACO['O']][node_index_map_ACO['O'+str(i)]] = 0

    for i in range(1, team_num-1):
        adj_matrix_ACO[node_index_map_ACO['O'+str(i+1)]][node_index_map_ACO['O'+str(i)]] = 0
        adj_matrix_ACO[node_index_map_ACO['O'+str(i+1)]][node_index_map_ACO['O'+str(i)]] = 0

    return nodes_ACO, adj_matrix_ACO, node_index_map_ACO

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
                    dist[i][j] = round(dist[i][k] + dist[k][j],1)
                    path[i][j] = path[k][j]
    return dist, path

def path_expansion(list, Path):
    for i in range(len(list)-1):
        extra_node = Path[list[i]][list[i+1]]
        if extra_node != list[i]:
            list.insert(i + 1, extra_node)
            i -= 1
    return list

def generate_random_path(team_num = 3):
    random_path = [x for x in range(0, 53)] 
    random_path.remove(49)
    for i in range(team_num - 1):
        random_path.append(49)
    random.shuffle(random_path)
    random_path.insert(0,49)
    random_path.append(49)
    return random_path

def calculate_path_cost(path, dist, true_cost=False, team_num = 3, penalty = 0.5):
    
    cost = 0
    for i in range(len(path)-1):
        cost += dist[path[i]][path[i+1]]
    
    if true_cost==False:
        paths = split_path(path, team_num = team_num, expand = False)

        # cost_ = cost
        max_cost = float("-inf")
        min_cost = float("inf")
        for temp_path in paths:
            temp_cost = calculate_path_cost(temp_path, dist, true_cost=True)
            max_cost = max(temp_cost, max_cost)
            min_cost = min(temp_cost, min_cost)
            # cost += 100 * max((len(temp_path)-2-(56/team_num)),0)
            # cost += 0.1 * abs(temp_cost-(cost_/team_num))
        cost += penalty*(max_cost-min_cost) #/max_cost
    return cost

def split_path(path, Path=None ,team_num = 3, expand = True):
    path_ = path.copy()
    del path_[len(path)-1]
    del path_[0]

    paths = []
    for i in range(team_num - 1):
        temp_path = path_[:path_.index(49)+1]
        temp_path.insert(0,49)
        path_ = path_[path_.index(49)+1:]
        if expand:
            paths.append(path_expansion(temp_path, Path))
        else:
            paths.append(temp_path)

    path_.insert(0,49)
    path_.append(49)
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