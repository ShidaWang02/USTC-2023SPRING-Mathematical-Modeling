'''
dists floyd处理后邻接矩阵
stay_time 留的时间
node_index_map 索引
team_nums 队伍数量
velocity 城市间移动速度
consider_stay true为计算时间 false为计算路径

get_answer()为根据consider_stay打印时间或路径,返回值为一个含有三个数组的二维数组表示path
'''
class Greedy(object):
    def __init__(self,dists,stay_time,node_index_map,team_nums,velocity = 35,consider_stay = True):
        self.dists = dists
        self.stay_time = stay_time
        self.team_nums = team_nums
        self.node_index_map = node_index_map
        self.consider_stay = consider_stay
        self.velocity = velocity

    def goal(self,start,now,going):
        '''
        目标函数表示去往下一个地点后立即返回所产生的时间或路程
        '''
        if self.consider_stay:
            return (self.dists[now][going] + self.dists[going][start])/self.velocity + self.stay_time[going]
        else:
            return self.dists[now][going] + self.dists[going][start]
    
    def get_answer(self):
        length = len(self.dists)
        path = [[] for i in range(self.team_nums)]
        vis = set()
        for i in [49,53,54,55,56]:
            vis.add(i) 
        point = 0
        for i in range(self.team_nums):
            path[i].append(49)
        while len(vis) != 57:
            min_goal = 100000
            going = -1
            for j in range(length):
                now = path[point][-1]
                if j not in vis :
                    goal = self.goal(49,now,j)
                    if goal < min_goal:
                        min_goal = goal
                        going = j
            if going == -1 or going in vis:
                break
            path[point].append(going)
            vis.add(going)
            point = (point + 1)%self.team_nums
        for i in range(self.team_nums):
            path[i].append(49)

        if self.consider_stay:
            self.calculate_time_cost(paths=path)
        else:
            self.calculate_path_cost(paths=path)
        return path
    
    def calculate_one_team_time_cost(self,temp_path, velocity=35):
        dist = self.dists
        stay_time = self.stay_time
        temp_cost = 0
        for i in range(len(temp_path)-1):
            temp_cost += dist[temp_path[i]][temp_path[i+1]]/velocity
            temp_cost += stay_time[temp_path[i]]
        return temp_cost

    def calculate_time_cost(self,paths):
        total_cost = 0
        node_index_map = self.node_index_map
        for j in range(len(paths)):
            temp_length = round(self.calculate_one_team_time_cost(paths[j],velocity=self.velocity),1)
            temp_path = [list(node_index_map.keys())[list(node_index_map.values()).index(i)] for i in paths[j]]
            print("最短路径"+str(j)+":", temp_path, "\n经过节点个数:", len(temp_path),"总时间",temp_length)
            total_cost = max(temp_length,total_cost)
        print("总时间:", total_cost)

    def calculate_single_path_cost(self,path):
        cost = 0
        for i in range(len(path)-1):
            cost += self.dists[path[i]][path[i+1]] 
        return cost
    
    def calculate_path_cost(self,paths):
        total_cost = 0
        node_index_map = self.node_index_map
        for j in range(len(paths)):
            temp_length = round(self.calculate_single_path_cost(paths[j]),1)
            temp_path = [list(node_index_map.keys())[list(node_index_map.values()).index(i)] for i in paths[j]]
            print("最短路径"+str(j)+":", temp_path, "\n经过节点个数:", len(temp_path),"路径长度",temp_length)
            total_cost = total_cost + temp_length
        print("路径长度:", total_cost)

