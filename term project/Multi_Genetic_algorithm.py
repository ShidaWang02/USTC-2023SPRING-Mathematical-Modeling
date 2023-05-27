from Functions import *
import random
import numpy as np
random.seed(1)
# 选择
def selection(population_size, population, dist, stay_time, team_num = 3, method = 1, penalty = 0.5):
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
            group.sort(key=lambda path: calculate_path_cost(path, dist, true_cost=False, team_num = team_num, penalty = penalty))
        elif method ==2:
            group.sort(key=lambda path: calculate_time_cost(path, dist, stay_time, true_cost=False, team_num = team_num))
        # 取出获胜者
        winners += group[:group_winner]
    population = winners
    return winners

# 交叉
def crossover(population,mutation_probability = 0.5):
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
        if random.random() < mutation_probability: 
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
def multi_genetic_algorithm(dist, stay_time, population_size=100, iterations=100, team_num = 3, method =1):
    # 种群大小
    size = population_size
    # 迭代次数
    iter = 0
    # 初始化种群
    population1 = []
    population2 = []
    population3 = []
    population4 = []
    all_population = []
    best_cost_list = []
    mutation_probability = 0.3
    penalty = 0.1
    for i in range(size):
        population1.append(generate_random_path(team_num = team_num, path_len = len(dist)))
        population2.append(generate_random_path(team_num = team_num, path_len = len(dist)))
        population3.append(generate_random_path(team_num = team_num, path_len = len(dist)))
        population4.append(generate_random_path(team_num = team_num, path_len = len(dist)))
    # 迭代直到达到最大迭代次数
    while iter < iterations:
        mutation_probability += 0.7/iterations
        penalty += 0.4/iterations
        # 交叉
        population1 = crossover(population1,mutation_probability)
        population2 = crossover(population2,mutation_probability)
        population3 = crossover(population3,mutation_probability)
        population4 = crossover(population4,mutation_probability)

        population1 = crossover(population1,mutation_probability)
        population2 = crossover(population2,mutation_probability)
        population3 = crossover(population3,mutation_probability)
        population4 = crossover(population4,mutation_probability)
        # 选择
        population1 = selection(population_size, population1, dist, stay_time, team_num = team_num, method = method, penalty = penalty)
        population2 = selection(population_size, population2, dist, stay_time, team_num = team_num, method = method, penalty = penalty)
        population3 = selection(population_size, population3, dist, stay_time, team_num = team_num, method = method, penalty = penalty)
        population4 = selection(population_size, population4, dist, stay_time, team_num = team_num, method = method, penalty = penalty)
        all_population = population1 + population2 + population3 + population4

        if method == 1:
            all_population.sort(key=lambda path: calculate_path_cost(path, dist, true_cost=False, team_num = team_num, penalty = penalty))
            best_cost = calculate_path_cost(all_population[0], dist, true_cost=False, team_num = team_num, penalty = penalty)
        elif method == 2:
            all_population.sort(key=lambda path: calculate_time_cost(path, dist, stay_time, true_cost=False, team_num = team_num))
            best_cost = calculate_time_cost(all_population[0], dist, stay_time, true_cost=False, team_num = team_num)

        best_cost_list.append(best_cost)
         
        if iter % (iterations // 50) == 0:
            all_population = all_population[:population_size]
            population1 = crossover(population1+all_population,mutation_probability)
            population2 = crossover(population2+all_population,mutation_probability)
            population3 = crossover(population3+all_population,mutation_probability)
            population4 = crossover(population4+all_population,mutation_probability)
            population1 = selection(population_size, population1, dist, stay_time, team_num = team_num, method = method, penalty = penalty)
            population2 = selection(population_size, population2, dist, stay_time, team_num = team_num, method = method, penalty = penalty)
            population3 = selection(population_size, population3, dist, stay_time, team_num = team_num, method = method, penalty = penalty)
            population4 = selection(population_size, population4, dist, stay_time, team_num = team_num, method = method, penalty = penalty)
            
        iter += 1   
       
    if method == 1:
        all_population.sort(key=lambda path: calculate_path_cost(path, dist, true_cost=False, team_num = team_num, penalty = penalty))
        best_cost = calculate_path_cost(all_population[0], dist, true_cost=True, team_num = team_num)
    elif method == 2:
        all_population.sort(key=lambda path: calculate_time_cost(path, dist, stay_time, true_cost=False, team_num = team_num))
        best_cost = calculate_time_cost(all_population[0], dist, stay_time, true_cost=True, team_num = team_num)

    return all_population[0], round(best_cost,2), iterations, best_cost_list
