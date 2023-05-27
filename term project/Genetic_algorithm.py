from Functions import *
import random
import numpy as np
random.seed(1)
# 选择
def selection(population_size, population, dist, stay_time, team_num = 3, method = 1):
    group_num = 20  # 小组数
    group_size = len(population) // group_num  # 每小组人数
    group_winner = population_size // group_num  # 每小组获胜人数
    winners = []  # 锦标赛结果
    index = 0
    random.shuffle(population)
    for i in range(group_num):
        group = []
        for j in range(group_size):
            # 随机组成小组
            # player = random.choice(population)
            player = population[index]
            index += 1
            group.append(player)
        if method == 1:
            group.sort(key=lambda path: calculate_path_cost(path, dist, true_cost=False, team_num = team_num))
        elif method ==2:
            group.sort(key=lambda path: calculate_time_cost(path, dist, stay_time, true_cost=False, team_num = team_num))
        # 取出获胜者
        winners += group[:group_winner]
    population = winners
    return winners

# 交叉
def crossover(population):
    # 交叉次数
    size = len(population)
    # 交叉
    random.shuffle(population)
    for i in range(0, size-1, 2):
        genes1 = population[i].copy()
        genes2 = population[i+1].copy()
        del genes1[len(genes1)-1]
        del genes1[0]
        del genes2[len(genes2)-1]
        del genes2[0]
        index1 = random.randint(0, len(genes1) - 2)
        index2 = random.randint(index1, len(genes1) - 1)
        pos1_recorder = {value: idx for idx, value in enumerate(genes1)}
        pos2_recorder = {value: idx for idx, value in enumerate(genes2)}
        # 交叉
        for j in range(index1, index2):
            value1, value2 = genes1[j], genes2[j]
            pos1, pos2 = pos1_recorder[value2], pos2_recorder[value1]
            genes1[j], genes1[pos1] = genes1[pos1], genes1[j]
            genes2[j], genes2[pos2] = genes2[pos2], genes2[j]
            pos1_recorder[value1], pos1_recorder[value2] = pos1, j
            pos2_recorder[value1], pos2_recorder[value2] = j, pos2

        genes1.insert(0,0)
        genes1.append(0)
        genes2.insert(0,0)
        genes2.append(0)
        if random.random() < 0.5: 
            population.append(mutation(genes1))
            population.append(mutation(genes2))
        else:
            population.append(genes1)
            population.append(genes2)
    return population

# 变异
def mutation(genes):
    old_genes = genes.copy()
    index1 = random.randint(1, len(genes) - 3)
    index2 = random.randint(index1, len(genes) - 2)
    genes_mutate = old_genes[index1:index2]
    genes_mutate.reverse()
    genes = old_genes[:index1] + genes_mutate + old_genes[index2:]
    return genes

# 遗传算法
def genetic_algorithm(dist, stay_time, population_size=100, iterations=100, team_num = 3, method =1):
    # 种群大小
    size = population_size
    # 迭代次数
    iter = 0
    # 初始化种群
    population = []
    best_cost_list = []

    for i in range(size):
        population.append(generate_random_path(team_num = team_num, path_len = len(dist)))
    # 迭代直到达到最大迭代次数
    while iter < iterations:
       
        # 交叉
        population = crossover(population)
        # population = crossover(population)
        # 选择
        population = selection(population_size, population, dist, stay_time, team_num = team_num, method = method)
        iter += 1
        # 返回最优解
        if method == 1:
            population.sort(key=lambda path: calculate_path_cost(path, dist, true_cost=False, team_num = team_num))
            best_cost = calculate_path_cost(population[0], dist, true_cost=False, team_num = team_num)
        elif method == 2:
            population.sort(key=lambda path: calculate_time_cost(path, dist, stay_time, true_cost=False, team_num = team_num))
            best_cost = calculate_time_cost(population[0], dist, stay_time, true_cost=False, team_num = team_num)

        best_cost_list.append(best_cost)
        
    if method == 1:
        best_cost = calculate_path_cost(population[0], dist, true_cost=True, team_num = team_num)
    elif method == 2:
        best_cost = calculate_time_cost(population[0], dist, stay_time, true_cost=True, team_num = team_num)

    return population[0], round(best_cost,2), iterations, best_cost_list
