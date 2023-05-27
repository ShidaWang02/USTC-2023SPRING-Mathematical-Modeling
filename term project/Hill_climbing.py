from Functions import *
def hill_climbing(dist, stay_time, method=1, team_num = 3):
    best_cost_list = []
    # 全局最优解
    best_path = generate_random_path(team_num = team_num, path_len = len(dist))
    if method == 1:
        best_cost = calculate_path_cost(best_path, dist, true_cost=False, team_num = team_num)
        
    elif method == 2:
        best_cost = calculate_time_cost(best_path, dist, stay_time, true_cost=False, team_num = team_num)

    best_cost_list.append(best_cost)
    # 迭代次数
    iterations = 0
    while iterations < 200000:
        new_path = best_path.copy()
        index1 = random.randint(1,len(best_path)-2)
        index2 = random.randint(1,len(best_path)-2)
        new_path[index1], new_path[index2] = new_path[index2], new_path[index1]
        # 计算新解的花销
        if method == 1:
            new_cost = calculate_path_cost(new_path, dist, true_cost=False, team_num = team_num)
        elif method == 2:
            new_cost = calculate_time_cost(new_path, dist, stay_time, true_cost=False, team_num = team_num)
        # 如果新解更优，则接受新解
        if new_cost < best_cost:
            best_path = new_path
            best_cost = new_cost
        iterations += 1
        best_cost_list.append(best_cost)

    if method == 1:
        best_cost = calculate_path_cost(best_path, dist, true_cost=True, team_num = team_num)
    elif method == 2:
        best_cost = calculate_time_cost(best_path, dist, stay_time, true_cost=True, team_num = team_num)
    return best_path, round(best_cost,2), iterations, best_cost_list