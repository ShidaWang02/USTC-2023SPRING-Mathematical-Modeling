from Functions import *
import random
import math

def calculate_velocity(paricle1,paricle2):
    genes1 = paricle1.copy()
    genes2 = paricle2.copy()
    del genes1[len(genes1)-1]
    del genes1[0]
    del genes2[len(genes2)-1]
    del genes2[0]
    pos1_recorder = {value: idx for idx, value in enumerate(genes1)}
    velocity = []
    for j in range(len(genes1)):
        value1, value2 = genes1[j], genes2[j]
        pos1 = pos1_recorder[value2]
        genes1[j], genes1[pos1] = genes1[pos1], genes1[j]
        velocity.append([j,pos1])
        pos1_recorder[value1], pos1_recorder[value2] = pos1, j
        
    return velocity

def calculate_paricle(paricle,velocity):
    paricle = paricle.copy()

    del paricle[len(paricle)-1]
    del paricle[0]

    for i in range(len(velocity)):
        if velocity[i] == [-1,-1]:
            continue
        pos1,pos2 = velocity[i]
        paricle[pos1], paricle[pos2] = paricle[pos2], paricle[pos1]
    
    paricle.insert(0,0)
    paricle.append(0)

    return paricle

def generate_random_velocity(paricle, team_num = 3):
    another_paricle = generate_random_path(team_num = team_num)
    velocity = calculate_velocity(paricle,another_paricle)
    return velocity

def mutation(genes):
    old_genes = genes.copy()
    index1 = random.randint(1, len(genes) - 3)
    index2 = random.randint(index1, len(genes) - 2)
    genes_mutate = old_genes[index1:index2]
    genes_mutate.reverse()
    genes = old_genes[:index1] + genes_mutate + old_genes[index2:]
    return genes

# 粒子群算法
def particle_group_algorithm(dist, stay_time, particles_size=1000, iterations=100, team_num = 3, method =1):
    # 种群大小
    size = particles_size
    # 迭代次数
    iter = 0
    # 初始化粒子群
    particles = []
    velocity = []
    personal_best_cost = []
    personal_best_particle = []
    best_cost_list = []
    for i in range(size):
        particle = generate_random_path(team_num = team_num)   
        particles.append(particle)
        personal_best_particle.append(particle)
        velocity.append(generate_random_velocity(particle, team_num = team_num))
        if method == 1:
            personal_best_cost.append(calculate_path_cost(particle, dist, true_cost=False, team_num = team_num))
        elif method == 2:
            personal_best_cost.append(calculate_time_cost(particle, dist, stay_time, true_cost=False, team_num = team_num))
    
    if method == 1:
        particle_ = particles.copy()
        particle_.sort(key=lambda path: calculate_path_cost(path, dist, true_cost=False, team_num = team_num))
        global_best_particle = particle_[0]
        global_best_cost = calculate_path_cost(particle_[0], dist, true_cost=False, team_num = team_num)
        best_cost_list.append(global_best_cost)

    elif method == 2:
        particle_ = particles.copy()
        particle_.sort(key=lambda path: calculate_time_cost(path, dist, stay_time, true_cost=False, team_num = team_num))
        global_best_particle = particle_[0]
        global_best_cost = calculate_time_cost(particle_[0], dist, stay_time, true_cost=False, team_num = team_num)
        best_cost_list.append(global_best_cost)

    w = 1
    c1 = 0.1
    c2 = 0.1

    # 迭代直到达到最大迭代次数
    while iter < iterations:
        # print(np.array(particles)[0,:10])
        # print(np.array(global_best_particle)[:10])
        w -= 0.2/iterations
        c1 += 0.2/iterations
        c2 += 0.2/iterations
        for i in range(len(particles)):

            velocity_1 = calculate_velocity(particles[i],personal_best_particle[i])
            velocity_2 = calculate_velocity(particles[i],global_best_particle)

            new_velocity = velocity[i].copy()
            
            for j  in range(len(velocity[i])):
                if random.random()>w:
                    new_velocity[j] = [-1,-1]
            for j in range(len(velocity_1)):
                if random.random()<=c1:

                    new_velocity[j] = velocity_1[j]
            for j in range(len(velocity_2)):
                if random.random()<=c2:
                    new_velocity[j] = velocity_2[j]
            
            
            velocity[i] = new_velocity
            particles[i] = calculate_paricle(particles[i],velocity[i])
            
            if random.random() < 0.25:
                particles[i] = mutation(particles[i])

            if method == 1:
                particle_cost = calculate_path_cost(particles[i], dist, true_cost=False, team_num = team_num)

            elif method == 2:
                particle_cost = calculate_time_cost(particles[i], dist, stay_time, true_cost=False, team_num = team_num)

            if particle_cost < personal_best_cost[i]:
                personal_best_cost[i] = particle_cost
                personal_best_particle[i] = particles[i]
            
            if particle_cost < global_best_cost:
                global_best_particle = particles[i]
                global_best_cost =  particle_cost

        iter += 1
        best_cost_list.append(global_best_cost)
        # print(global_best_cost)
        
    if method == 1:
        global_best_cost = calculate_path_cost(global_best_particle, dist, true_cost=True, team_num = team_num)
    elif method == 2:
        global_best_cost = calculate_time_cost(global_best_particle, dist, stay_time, true_cost=True, team_num = team_num)

    return global_best_particle, round(global_best_cost,2), iterations, best_cost_list
