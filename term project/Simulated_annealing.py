from Functions import *
import random
import math
# 模拟退火算法
def simulated_annealing(dist, stay_time, method=1, team_num = 3, inti_path = None):
    # 初始温度
    temperature = 10000
    # 降温速度
    cooling_rate = 0.0001
    # 初始解
    if inti_path == None:
        current_path = generate_random_path(team_num = team_num, path_len = len(dist))
    else:
        current_path = inti_path
    # 当前解的路径长度
    if method == 1:
        current_cost = calculate_path_cost(current_path, dist, true_cost=False, team_num = team_num)
    elif method == 2:
        current_cost = calculate_time_cost(current_path, dist, stay_time, true_cost=False, team_num = team_num)
    
    # 全局最优解
    best_path = current_path
    best_cost = current_cost
    best_cost_list = [best_cost]
    # 迭代次数
    iterations = 0
    # 迭代直到温度降到0
    while temperature > 0.0001:
        # 随机交换两个城市的位置
        new_path = current_path.copy()
        index1 = random.randint(1,len(best_path)-2)
        index2 = random.randint(1,len(best_path)-2)
        new_path[index1], new_path[index2] = new_path[index2], new_path[index1]
        # 计算新解的花销
        if method == 1:
            new_cost = calculate_path_cost(new_path, dist, true_cost=False, team_num = team_num)
        elif method == 2:
            new_cost = calculate_time_cost(new_path, dist, stay_time, true_cost=False, team_num = team_num)
        # 如果新解更优，则接受新解
        if new_cost < current_cost:
            current_path = new_path
            current_cost = new_cost
            # 更新全局最优解
            if current_cost < best_cost:
                best_path = current_path
                best_cost = current_cost
        # 否则以一定概率接受新解
        else:
            delta = new_cost - current_cost
            acceptance_probability = math.exp(-delta / temperature)
            if random.random() < acceptance_probability:
                current_path = new_path
                current_cost = new_cost
        # 降温
        temperature *= 1 - cooling_rate
        iterations += 1
        best_cost_list.append(best_cost)

    if method == 1:
        best_cost = calculate_path_cost(best_path, dist, true_cost=True, team_num = team_num)
    elif method == 2:
        best_cost = calculate_time_cost(best_path, dist, stay_time, true_cost=True, team_num = team_num)

    return best_path, round(best_cost,2), iterations, best_cost_list

