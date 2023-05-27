import Functions_ACO
import random
import numpy as np
import copy
import sys

class Ant(object):

    # 初始化
    def __init__(self,ID,city_num, team_num,distance_graph,stay_time,pheromone_graph,alpha,beta,method=1,penalty=0.5):

        self.ID = ID                 # ID
        self.city_num = city_num     # 城市数量
        self.team_num = team_num     # 队伍数量
        self.distance_graph = distance_graph     # 距离矩阵
        self.stay_time = stay_time   # 停留时间矩阵
        self.pheromone_graph = pheromone_graph   # 信息素矩阵
        self.alpha = alpha           # 信息素重要程度
        self.beta = beta             # 启发式因子重要程度
        self.method = method         # 1为路径长度，2为时间
        self.penalty = penalty       # 惩罚系数
        self.__clean_data()          # 初始化出生点

    # 初始数据
    def __clean_data(self):

        self.path = []               # 当前蚂蚁的路径           
        self.total_distance = 0.0    # 当前路径的总距离
        self.penalty_distance = 0.0  # 当前路径的惩罚距离
        self.total_time = 0.0        # 当前路径的总时间
        self.move_count = 0          # 移动次数
        self.current_city = -1       # 当前停留的城市
        self.open_table_city = [True for i in range(self.city_num)] # 探索城市的状态

        city_index = random.randint(0,self.city_num-1) # 随机初始出生点
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    # 选择下一个城市
    def __choice_next_city(self):

        next_city = -1
        select_citys_prob = [0.0 for i in range(self.city_num)]  #存储去下个城市的概率
        total_prob = 0.0

        # 获取去下一个城市的概率
        for i in range(self.city_num):
            if self.open_table_city[i]:
                try :
                    # 计算概率：与信息素浓度成正比，与距离成反比
                    select_citys_prob[i] = pow(self.pheromone_graph[self.current_city][i], self.alpha) * pow((1.0/self.distance_graph[self.current_city][i]), self.beta)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError as e:
                    print ('Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID = self.ID, current = self.current_city, target = i))
                    sys.exit(1)

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(self.city_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        if (next_city == -1):
            next_city = random.randint(0, self.city_num - 1)
            while ((self.open_table_city[next_city]) == False):  # if==False,说明已经遍历过了
                next_city = random.randint(0, self.city_num - 1)

        # 返回下一个城市序号
        return next_city

    # 计算路径总距离
    def __cal_total_distance(self):

        temp_distance = 0.0

        for i in range(1, self.city_num):
            start, end = self.path[i], self.path[i-1]
            temp_distance += self.distance_graph[start][end]

        # 回路
        end = self.path[0]
        temp_distance += self.distance_graph[start][end]
        self.total_distance = temp_distance

    def __cal_penalty_distance(self):
        # 调整path 
        path = self.path.copy()
        path = path[path.index(49):]+path[:path.index(49)]
        to_change = [50+i for i in range(self.team_num-1)]
        for i in range(len(path)):
            if path[i] in to_change:
                path[i] = 49
            if path[i] > 49 + self.team_num - 1:
                path[i] -= (self.team_num - 1)
        path.append(49)
        self.penalty_distance = Functions_ACO.calculate_path_cost(path, dist=np.delete(np.delete(self.distance_graph,to_change,axis = 0),to_change,axis=1), true_cost=False,team_num=self.team_num,penalty=self.penalty)
        # print("惩罚距离:",self.penalty_distance)

    def __cal_total_time(self):
        # 调整path 
        path = self.path.copy()
        path = path[path.index(49):]+path[:path.index(49)]
        to_change = [50+i for i in range(self.team_num-1)]
        for i in range(len(path)):
            if path[i] in to_change:
                path[i] = 49
            if path[i] > 49 + self.team_num - 1:
                path[i] -= (self.team_num - 1)
        path.append(49)
        self.total_time = Functions_ACO.calculate_time_cost(path, dist=np.delete(np.delete(self.distance_graph,to_change,axis = 0),to_change,axis=1), stay_time = self.stay_time,true_cost=True,team_num=self.team_num)
        # print("总时间:",self.total_time)

    # 移动操作
    def __move(self, next_city):

        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += self.distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    # 搜索路径
    def search_path(self):

        # 初始化数据
        self.__clean_data()

        # 搜素路径，遍历完所有城市为止
        while self.move_count < self.city_num:
            # 移动到下一个城市
            next_city =  self.__choice_next_city()
            self.__move(next_city)

        # 计算路径总惩罚长度
        self.__cal_total_distance()
        if self.method == 1:
            self.__cal_penalty_distance()
        elif self.method == 2:
            self.__cal_total_time()

class ACO(object):

    def __init__(self, city_num, team_num, distance, stay_time, ant_num = 50, alpha = 1.0, beta = 2.0, rho = 0.5, Q = 1, iter_max = 200, method = 1,penalty = 0.5):

        self.city_num = city_num
        self.team_num = team_num
        self.ant_num = ant_num
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.penalty = penalty
        self.iter_max = iter_max

        # 获得距离矩阵
        self.distance_graph = distance
        self.stay_time = stay_time
        self.method = method

        self.penalty_dists = []
        self.times = []


    # 初始化
    def new(self, ):

        # 初始城市之间的信息素
        self.pheromone_graph = np.ones((self.city_num, self.city_num))
        self.ants = [Ant(ID, self.city_num, self.team_num, self.distance_graph,self.stay_time,self.pheromone_graph,self.alpha,self.beta,method=self.method,penalty = self.penalty) for ID in range(self.ant_num)]  # 初始蚁群
        self.best_ant = Ant(-1, self.city_num, self.team_num, self.distance_graph,self.stay_time,self.pheromone_graph,self.alpha,self.beta,method=self.method,penalty = self.penalty)                              # 初始最优解
        self.best_ant.total_distance = 1 << 31               # 初始最大距离
        self.best_ant.penalty_distance = 1 << 31               # 初始最大惩罚距离
        self.best_ant.total_time = 1 << 31                   # 初始最大时间
        self.iter = 1                                        # 初始化迭代次数


    # 开始搜索
    def search_path(self, ):
        for ant in self.ants:
            # 搜索一条路径
            ant.search_path()
            # 与当前最优蚂蚁比较
            if self.method == 1:
                if ant.penalty_distance < self.best_ant.penalty_distance:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
            elif self.method == 2:
                if ant.total_time < self.best_ant.total_time:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
        # 更新信息素
        self.__update_pheromone_gragh()
        # 保存最优解
        self.penalty_dists.append(self.best_ant.penalty_distance)
        self.times.append(self.best_ant.total_time)
        # if self.iter % 10 == 0:
        #     if self.method ==1:
        #         print (u"迭代次数：",self.iter,u"最佳路径总距离：",int(self.best_ant.total_distance))
        #     elif self.method == 2:
        #         print (u"迭代次数：",self.iter,u"最佳路径总时间：",int(self.best_ant.total_time))
        self.iter += 1

    # 更新信息素
    def __update_pheromone_gragh(self):
        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = np.zeros((self.city_num, self.city_num))
        for ant in self.ants:
            for i in range(1,self.city_num):
                start, end = ant.path[i-1], ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                if self.method == 1:
                    temp_pheromone[start][end] += self.Q / ant.penalty_distance
                elif self.method == 2:
                    temp_pheromone[start][end] += self.Q / ant.total_time
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        for i in range(self.city_num):
            for j in range(self.city_num):
                self.pheromone_graph[i][j] = self.pheromone_graph[i][j] * self.rho + temp_pheromone[i][j]

    def change_path(self, path):
        path = path[path.index(49):]+path[:path.index(49)]
        to_change = [50+i for i in range(self.team_num-1)]
        for i in range(len(path)):
            if path[i] in to_change:
                path[i] = 49
            if path[i] > 49 + self.team_num - 1:
                path[i] -= (self.team_num - 1)
        path.append(49)
        return path

