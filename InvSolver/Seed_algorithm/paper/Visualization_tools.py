from InvSolver.Seed_algorithm.paper.Tools import data_tools
import matplotlib
import matplotlib.pyplot as plt
import scienceplots
class Record_Tools:
    def __init__(self,moudle_file,mesh_file,out_log_file):
        self.moudle_data_tool=data_tools(moudle_file,mesh_file )
        self.mesh_file=mesh_file
        self.loger=open(out_log_file,'w')
        self.res_data_tools=[]
        self.error=[]
        self.TP=[]
        self.FN=[]
        self.TN=[]
        self.FP=[]
    def add_data(self,data_file):
        self.res_data_tools.append(data_tools(data_file, self.mesh_file))
    
    def calculate_indicators(self,Abnormal_body_rhos,Abnormal_body_rho_interval=0.3):
        # 假如正常区域密度2.65，异常区域密度为1.6，界限为0.3。那么2.3在正常区域就是异常，在异常区域就是被识别为正常
        """_summary_

        Args:
            Abnormal_body_rhos (list): 
            Abnormal_body_rho_interval (float, optional): _description_. Defaults to 0.3.
        """
        moudle_data=self.moudle_data_tool.get_data()
        for i in range(len(self.res_data_tools)):
            res_data=self.res_data_tools[i].get_data()
            count_TP=0#TP  # 
            count_FN=0#FN
            count_TN=0#TN
            count_FP=0#FP
            for j in range(len(moudle_data)):
                if moudle_data[j] in Abnormal_body_rhos:  # 实际上是异常
                    # 这里是以1.6为基准，在他附近视为异常
                    if abs(moudle_data[j]-res_data[j])<=Abnormal_body_rho_interval:  # 识别出为异常。 正确识别出的异常区域
                        count_TP+=1
                    else:
                        count_FN+=1   # 实际上是异常，识别出是异常。但是根据1.6基准没有看出来是不是异常
                else:  # 实际上是正常
                    # 这里是以2.65为基准，在他附近视为正常
                    # 假如附近为0.1.那么1.75在box内就会被视为正常，但是在box外就会被当做异常
                    if abs(moudle_data[j]-res_data[j])<=Abnormal_body_rho_interval:  # 识别出为正常。实际上是正常，识别出也是
                        count_TN+=1
                    else:
                        count_FP+=1  # 实际上是正常，但是识别出来是异常
            self.error.append(self.moudle_data_tool.calculation_results_gap(res_data))
            self.TP.append(count_TP)
            self.FN.append(count_FN)
            self.TN.append(count_TN)
            self.FP.append(count_FP)
            self.loger.write(str(self.error[-1])+" ")
            self.loger.write(str(count_TP)+" ")
            self.loger.write(str(count_FN)+" ")
            self.loger.write(str(count_TN)+" ")
            self.loger.write(str(count_FP)+" ")
            self.loger.write("\n")
    def clear_data(self):
        self.res_data_tools=[]
        self.error=[]
        self.TP=[]
        self.FN=[]
        self.TN=[]
        self.FP=[]
    def show_res_data(self,show=True):
        plt.style.use(['science','ieee', 'no-latex'])
        matplotlib.rc("font", family='FangSong')  # 使用代码帮助matplotlib识别中文字体仿宋
        
        # plt.rcParams['savefig.dpi'] = 1500  # 图片像素
        # plt.rcParams['figure.dpi'] = 150  # 分辨率
        # plt.rcParams['figure.figsize']=(5.8, 4.8)
        ymin=200
        ymax=1200
        fig, ax = plt.subplots()
        # ax.set_ylim(ymin=ymin,ymax=ymax)       
        
        ax.plot([i for i in range(len(self.error))],self.error , label="$\phi$$_e$")
        print("$\phi$$_e$: ",self.error[-1])
        ax.legend(
            # bbox_to_anchor=(1, 1),  # 图例边界框起始位置
                loc="upper right",  # 图例的位置
                ncol=1,  # 列数
                mode="None",  # 当值设置为“expend”时，图例会水平扩展至整个坐标轴区域
                borderaxespad=0,  # 坐标轴和图例边界之间的间距
                #    title="模型",  # 图例标题
                shadow=False,  # 是否为线框添加阴影
                fancybox=True)  # 线框圆角处理参数
        # ax.grid()
        ax.set_xlim(left=0)
        # ax.set_ylim(bottom=2.55,top=2.7)
        # 设置图表标题并给坐标轴加上标签。
        # ax.set_title("预测模型、理论模型、参考模型x方向的切片密度对比")
        ax.set_xlabel("迭代次数")
        ax.set_ylabel("预测模型与理论模型的差异$\phi$$_e$")
        # 设置刻度标记的大小
        ax.tick_params(axis='both')
        if show:
            plt.show()
        
        fig, ax = plt.subplots()
        # ymin=0
        # ymax=1
        # ax.set_ylim(ymin=ymin,ymax=ymax)       
        
        ax.plot([i for i in range(len(self.TP))],[self.TP[i]/(self.TP[i]+self.FN[i]) for i in range(len(self.TP))] ,label="查全率")
        print("查全率：",str(self.TP[-1]/(self.TP[-1]+self.FN[-1])))
        ax.plot([i for i in range(len(self.TP))],[self.TP[i]/(self.TP[i]+self.FP[i]) for i in range(len(self.TP))] ,label="查准率")
        print("查准率：",str(self.TP[-1]/(self.TP[-1]+self.FP[-1])))
        # ax.plot([i for i in range(len(self.TP))],[self.TP[i]/(self.TP[i]+self.FN[i]) for i in range(len(self.TP))] , linewidth=1,linestyle='--',c='r',label="敏感性")
        # ax.plot([i for i in range(len(self.TP))],[(self.TP[i]+self.TN[i])/(self.TP[i]+self.FN[i]+self.TN[i]+self.FP[i]) for i in range(len(self.TP))] , linewidth=1,linestyle='--',c='r',label="准确率")
        ax.legend(
            # bbox_to_anchor=(1, 1),  # 图例边界框起始位置
                loc="lower right",  # 图例的位置
                ncol=1,  # 列数
                mode="None",  # 当值设置为“expend”时，图例会水平扩展至整个坐标轴区域
                borderaxespad=0,  # 坐标轴和图例边界之间的间距
                #    title="模型",  # 图例标题
                shadow=False,  # 是否为线框添加阴影
                fancybox=True)  # 线框圆角处理参数
        # ax.grid()
        ax.set_xlim(left=0)
        # ax.set_ylim(bottom=2.55,top=2.7)
        # 设置图表标题并给坐标轴加上标签。
        # ax.set_title("预测模型、理论模型、参考模型x方向的切片密度对比", fontsize=14)
        ax.set_xlabel("迭代次数")
        ax.set_ylabel("查准率、查全率")
        # ax.set_ylabel("%")#平均密度
        # 设置刻度标记的大小
        ax.tick_params(axis='both')
        if show:
            plt.show()