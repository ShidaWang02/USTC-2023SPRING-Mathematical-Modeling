class Solver(object):
    def __init__(self,dists,stay_time,node_index_map,velocity = 35):
        self.dists = dists
        self.stay_time = stay_time
        self.node_index_map = node_index_map
        self.velocity = velocity

    def get_answer(self):
        length = len(self.dists)
        path = []
        ans = []
        vis = set()
        for i in [49,53,54,55,56]:
            vis.add(i) 
        path.append(49)    
        #计算Th
        Th = 0
        for i in range(length):
            path.append(i)
            path.append(49)
            cost = self.calculate_one_team_time_cost(temp_path = path)
            if cost > Th:
                Th = cost
            path.pop()
            path.pop()
        while len(vis) != length:
            path = [49]
            #取远点找路：
            temp_time = 0
            far_point = -1
            far_distance = 0
            for i in range(length):
                if i not in vis:
                    if len(vis)>40:
                        goal1 = self.dists[49][i] + self.stay_time[i]*self.velocity
                    else:
                        goal1 = self.dists[49][i]
                    if goal1  > far_distance:
                        far_point = i
                        far_distance =  goal1
            #判断差值
            path.append(far_point)
            path.append(49)
            temp_time = self.calculate_one_team_time_cost(temp_path = path)
            while Th - temp_time >1.0: 
                vis.add(far_point)
                flag = 1
                if Th - temp_time >2.0:
                    flag = 2
                if len(vis) == length:
                    break
                path.pop() #去掉49
                temp_time = 0
                now = far_point
                far_point = -1
                far_distance = -100000
                for i in range(length):
                    if i not in vis and self.stay_time[i]<=flag:
                        if len(vis)<22:
                            goal = self.dists[49][i] 
                        else:
                            goal = self.dists[49][i] - self.dists[now][i]
                        if goal  > far_distance:
                            path.append(i)
                            path.append(49)
                            temp_time = self.calculate_one_team_time_cost(temp_path = path)
                            if temp_time < Th:
                                far_point = i
                                far_distance =  goal
                            path.pop()
                            path.pop()

                path.append(far_point)
                path.append(49)
                temp_time = self.calculate_one_team_time_cost(temp_path = path)

            if Th >= temp_time-0.0001 and far_point!=-1:
                vis.add(far_point)
                ans.append(path)
            else:
                path.pop()
                path.pop()
                path.append(49)
                ans.append(path)
            
        self.calculate_time_cost(paths=ans)

        return ans
    
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
