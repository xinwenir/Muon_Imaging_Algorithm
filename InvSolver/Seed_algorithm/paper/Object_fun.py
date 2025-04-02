import copy
from InvSolver.Seed_algorithm.paper.Tools import data_tools
import scipy.sparse
import numpy as np
import math
from InvSolver.Seed_algorithm.paper.Setting import  smooth_all_multiple, punishment_Search_distancevalue_multiple,prompt_value_multiple
class Obj_fun_Tools:
    def __init__(self):
        self.min_fun=None
        self.min_fun_x=None
        
    def clear_history(self):
        self.min_fun=None
        self.min_fun_x=None
    
    
    def objective_fun(self,x,seed_js,G,d,derrs,refs,bounds,distance,ancestors_seeds_js,issmooth,seeds_neighbor_js,data_tool:data_tools,need_bound=False,noise=False):
        _fun_x=copy.copy(x)
        x=np.array([x]).T
        noise_value=0
        if noise:
            import random
            noise_value=1*random.random()
        #misfit
        res=np.linalg.linalg.norm(np.dot(G,x)-(d+noise_value))
        for i in range(len(x)):
            #增加惩罚使得seed不能搜索的过远
            diff_value=x[i]-refs[i]
            if distance>1:
                res+=punishment_Search_distancevalue_multiple*distance*diff_value**2
            else: 
                res+=0
            
            if need_bound:
                #使用激活函数增加上下限约束
                if x[i]>=bounds[i][0] and x[i]<=bounds[i][1]:
                    res+=0
                else:
                    if x[i]<bounds[i][0]:
                        res+=100*(x[i]-bounds[i][0])**2
                    else:
                        res+=100*(x[i]-bounds[i][1])**2
                
            #内点罚函数
            # if True:
            #     x[i]=max(x[i],bounds[i][0]+0.00001)
            #     x[i]=min(x[i],bounds[i][1]-0.00001)
            #     Upper_and_lower_bound*=((x[i]-bounds[i][0])*(bounds[i][1]-x[i]))/(bounds[i][1]-bounds[i][0])
            
            #目标函数增加促进该种子密度接近其祖先种子密度的约束
            if issmooth:
                res+=(x[i]- data_tool.get_value(ancestors_seeds_js[i]))**2*prompt_value_multiple
            
            #目标函数增加平滑性
            if issmooth:
                for seeds_neighbor_j in  seeds_neighbor_js[i]:
                    res+=smooth_all_multiple*(x[i]-refs[i]-(data_tool.get_value(seeds_neighbor_j)-data_tool.get_refs_value(seeds_neighbor_j)))**2
            
        # print(x,res)
        
        #记录当前的值和目标函数值
        if self.min_fun is None or self.min_fun>res:
            self.min_fun=res
            self.min_fun_x=_fun_x
        
        return res
    
    def objective_gun(self,x,seed_js,G,d,derrs,refs,bounds,distance,ancestors_seeds_js,issmooth,seeds_neighbor_js,data_tool,need_bound=False):
        x=np.array([x]).T
        #misfit
        res=np.dot(G.T,(np.dot(G,x)-d))
        for i in range(len(x)):
        
            #增加惩罚使得seed不能搜索的过远
            diff_value=x[i]-refs[i]
            if distance>1:
                res[i]+=punishment_Search_distancevalue_multiple*distance*diff_value*2
            else: 
                res[i]+=0
            #目标函数增加促进该种子密度接近其祖先种子密度的约束
            if issmooth:
                res[i]+=(x[i]-data_tool.get_value(ancestors_seeds_js[i]))*2*prompt_value_multiple
            #目标函数增加平滑性
            if issmooth:
                for seeds_neighbor_j in  seeds_neighbor_js[i]:
                    res[i]+=smooth_all_multiple*(x[i]-refs[i]-(data_tool.get_value(seeds_neighbor_j)-data_tool.get_refs_value(seeds_neighbor_j)))*2
           #使用激活函数增加上下限约束
            if need_bound:
                if x[i]>=bounds[i][0] and x[i]<=bounds[i][1]:
                    res[i]+=0
                else:
                    if x[i]<bounds[i][0]:
                        # res[i]-=100*(x[i]-bounds[i][0])*2
                        res[i]=-100
                    else:
                        # res[i]+=100*(x[i]-bounds[i][1])*2
                        res[i]=100
        # print(x,res)
        return res.T[0] 
        
        
        
            
    