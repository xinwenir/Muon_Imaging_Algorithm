"""
todo 注意，建议将setting.py中的punishment_diff_value_multiple设置为0 其功能用threshold代替。将punishment_Search_distancevalue_multiple设置为0其功能用max_count代替
"""

##"""论文2仿真"""
# start_data_file=r"E:\vscode\Muon_Imaging_Algorithm\data\zzg\output\topo\seed_result"#初始值
# refs_file=r"E:\vscode\Muon_Imaging_Algorithm\data\zzg\input\ZZG5_ref_direct1.den"
# mesh_file=r"E:\vscode\Muon_Imaging_Algorithm\data\zzg\input\ZZG5.msh"
# matrix_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Temp\%s"
# bounds_file=r"E:\vscode\Muon_Imaging_Algorithm\data\zzg\input\ZZG5_bnd_direct1.den"
# moudles_file=refs_file

# out_put_dir=r"E:\vscode\Muon_Imaging_Algorithm\data\paper2\Differences_in_contrast\data\Paper1.6\res\seed_res"
# max_count=10

# #268408城墙小房子 185437 CRB5_中心值 179895 CRB5_非中心 #第二篇仿真 88896
# # start_seed=[162472,162462,162837,235962,309087,309077]

# """
# zzg_topo选取的点
# -1170 260 172 
# -1120 230 160
# -1140 230 167
# -1100 260 166
# -1130 278 160
# -1120 240 158
# """

# start_seed=[
# # 118963,
# # 118709,
# # 163085,
# # 294338
# ]
# # zzg-topo
# punishment_diff_value_multiple=1 
# punishment_Search_distancevalue_multiple=0.006*1.7 #限制搜索距离
# prompt_value_multiple=1.00 #促使当前的体素密度接近原始seed 不宜太大除非异常体密度比较均匀
# misfit_all_multiple=1
# smooth_all_multiple=1.0 

# punishment_factor=0.0 #外点罚函数的因子

# threshold=0.2
# seed_Minimum_density_variation=0.1 #种子最小密度变化,小于该值将不能成为种子,该值必须小于threshold


# #刘国瑞Test--2023年6月20日
# start_data_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr_new_moudle\toy4_ref1.den"#初始值
# refs_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr_new_moudle\toy4_ref1.den"
# mesh_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr_new_moudle\toy4.msh"
# matrix_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Temp\%s"
# bounds_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr_new_moudle\toy4_bnd1.den"
# moudles_file=r"E:\vscode\Muon_Imaging_Algorithm\data\output\lgr_new_moudle\res\moudles"

# out_put_dir=r"E:\vscode\Muon_Imaging_Algorithm\data\output\lgr_new_moudle\seed_res"
# max_count=5

# start_seed=[
#     110194,
#     111130,
#     112066
# ]

# # start_seed=[
# # 446587,
# # 448459,
# # 450332
# # ]

# punishment_diff_value_multiple=1 
# punishment_Search_distancevalue_multiple=0 #0.006*1.7 #限制搜索距离
# prompt_value_multiple=0 #1.00 #促使当前的体素密度接近原始seed 不宜太大除非异常体密度比较均匀
# misfit_all_multiple = 1
# smooth_all_multiple=0#1.0 

# punishment_factor=0.0 #外点罚函数的因子

# threshold=0.65
# seed_Minimum_density_variation=0.5 #种子最小密度变化,小于该值将不能成为种子,该值必须小于threshold


"""国睿论文答复"""
# 268408城墙小房子 185437 CRB5_中心值 179895 CRB5_非中心 #第二篇仿真 88896
# ZZG5.msh
# topo 坑: 162472, 162462, 162837, 235962, 309087, 309077
# ball1: 532229
# caikong1: 1401212, 1415951, 1342453, 1297953; 1460338, 1459955, 1460561(边缘); 旁边： 956303, 956313, 956318
# qinru1: 1502956, 1435433(中间)
# D5ball: 1032243
# D3D4后面： 181724, 181732, 122724

# ZZG6.msh
# topo: 162838, 221338 (threshold 2.0)
# ball: 517604, 561478, 634601, 693225, 560853, 648730, 678105, 707605, 766606 (threshold 0.3)
# caikong1: 1341713, 1341716, 1401582, 1401592, 1431078, 1431086, 1327959, 1357339, 1342835, 1416449,
#               1401578, 1401586, 1342827, 1342836
#   (threshold = 0.15)
# caikong1旁: 941678, 1029673, 1029675, 1044929, 1045926, 1074668, 1118047, 1104038; 偏下: 1060057, 1060183 (threshold 0.1)
# D3D4后面: 226096, 226095, 270092, 270219, 211973, 212222, 226850  (threshold 2.4)
# D6: 856616, 871615, 871618, 842117, 886616, 901238   (threshold 2.0)
# caikong2: 1209724, 1001220, 926470, 1016224, 1060601, 1060848, 942468  (threshold 1.0)
# gold mine
# D4: 370370, 355740, 355985, 281860, 281864, 341864,
# D3: 385732, 385981, 371361, 400859, 474740, 489743, 430362, 416109, 504614, 518987, 416230, 357602
# D2: 579727, 579732, 550971, 506971, 520971, 550975, 506975, 520975, 652735, 682610, 667733, 653103,
#               638599, 580341, 521837, 477457, 506706, 492218, 609470, 477716, 492585, 448711, 461601, 711246
#               475718, 491097, 490481, 432715, 448328
#               682599, 522213, 683230, 712232, 609967, 551590, 668600, 507582, 610094, 448831
#               419828, 448328, 463959, 551586, 683346 (threshold = 0.2)

# syth9B test
#   1070971, 1075596, 1064596, 705346, 709970, 713721, 237346, 241971, 245721
# start_seed = [370370, 355740, 355985, 281860, 281864, 341864,
#               385732, 385981, 371361, 400859, 474740, 489743, 430362, 416109, 504614, 518987, 416230, 357602,
#               579727, 579732, 550971, 506971, 520971, 550975, 506975, 520975, 652735, 682610, 667733, 653103,
#               638599, 580341, 521837, 477457, 506706, 492218, 609470, 477716, 492585, 448711, 461601, 711246,
#               475718, 491097, 490481, 432715, 448328,
#               682599, 522213, 683230, 712232, 609967, 551590, 668600, 507582, 610094, 448831,
#               419828, 448328, 463959, 551586, 683346]
# start_seed = [370370, 355740, 355985, 281860, 281864, 341864,
#               385732, 385981, 371361, 400859, 474740, 489743, 430362, 416109, 504614, 518987, 416230, 357602,
#               579727, 579732, 550971, 506971, 520971, 550975, 506975, 520975, 652735, 682610, 667733, 653103,
#               638599, 580341, 521837, 477457, 506706, 492218, 609470, 477716, 492585, 448711, 461601, 711246,
#               475718, 491097, 490481, 432715, 448328,
#               682599, 522213, 683230, 712232, 609967, 551590, 668600, 507582, 610094, 448831,
#               419828, 448328, 463959, 551586, 683346]
# start_data_file = r"E:\vscode\Muon_Imaging_Algorithm\data\output\lgr\paper_dafu\goldmineD2\seed_result"
# refs_file = start_data_file
# mesh_file = r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr\paper_dafu\ZZG6.msh"
# matrix_file = r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr\paper_dafu\Temp\%s"
# bounds_file = r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr\paper_dafu\ZZG6_bnd_direct1.den"
# moudles_file = refs_file


# start_seed=[
# 385732, 385981, 371361, 400859, 474740, 489743, 430362, 416109, 504614, 518987, 416230, 357602
# ]
# max_count = 6
# out_put_dir = r"E:\vscode\Muon_Imaging_Algorithm\data\output\lgr\paper_dafu\goldmine"
# punishment_diff_value_multiple = 0.3
# punishment_Search_distancevalue_multiple = 0.05  # 限制搜索距离
# prompt_value_multiple = 0.00  # 促使当前的体素密度接近原始seed 不宜太大除非异常体密度比较均匀
# misfit_all_multiple = 1
# smooth_all_multiple = 0.5
# punishment_factor = 0.0  # 外点罚函数的因子

# threshold = 2
# seed_Minimum_density_variation = 0.2  # 种子最小密度变化,小于该值将不能成为种子,该值必须小于threshold

# max_count=30 
# out_put_dir=r"E:\vscode\Muon_Imaging_Algorithm\data\output\lgr\paper_dafu\goldmine"
# punishment_diff_value_multiple=0.2
# punishment_Search_distancevalue_multiple=0.005
# prompt_value_multiple=0.0
# misfit_all_multiple=1
# smooth_all_multiple=0.1
# punishment_factor=0.0
# threshold=2
# seed_Minimum_density_variation=0.13


# 刘国睿三个密度异常体仿真
# 268408城墙小房子 185437 CRB5_中心值 179895 CRB5_非中心 #第二篇仿真 88896 [47672,88888,130104]
# start_seed=[
#     110194,
#     111130,
#     112066
# ]

# max_count=20#或者10 
# out_put_dir=r"E:\vscode\Muon_Imaging_Algorithm\data\output\lgr\paper_dafu\sim1"
# punishment_diff_value_multiple=0.01
# punishment_Search_distancevalue_multiple=0.05
# prompt_value_multiple=0.0005
# misfit_all_multiple=1
# smooth_all_multiple=0.1
# punishment_factor=0.0
# threshold=2.65
# seed_Minimum_density_variation=0.07

# start_data_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr_new_moudle\toy4_ref1.den"#初始值
# refs_file=start_data_file
# mesh_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr_new_moudle\toy4.msh"
# matrix_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Temp\%s"
# bounds_file=r"E:\vscode\Muon_Imaging_Algorithm\data\Input\lgr_new_moudle\toy4_bnd1.den"
# moudles_file=r"E:\vscode\Muon_Imaging_Algorithm\data\output\lgr_new_moudle\res\moudles"

from InvSysTools.MyTools.myPrint import myPrint_Hint


class SeedSetting:
    def __init__(self):
        self.start_seed=[
            2030012, 2030283, 2030151, 2043417, 2003417, 2043551, 2016617, 2016616, 2016883, 1989879
        ]

        self.max_count = 10
        self.out_put_dir = r"E:\vscode\Muon_Imaging_Algorithm-master\data\Temp\seed_test"  # 反演结果的存储路径
        self.punishment_diff_value_multiple = 0.00  # 避免一步到位，具体见块坐标下降公式。现已被threshold参数替代
        self.punishment_Search_distancevalue_multiple = 0.02  # 限制搜索距离
        self.prompt_value_multiple = 0.01  # 促使当前的体素密度接近原始seed 不宜太大除非异常体密度比较均匀
        self.misfit_all_multiple = 1  # 不可修改
        self.smooth_all_multiple = 0.1  # 正则化因子
        # punishment_factor=0.0
        self.threshold = 1.0  # 单次下降所允许的最大值 用来替代punishment_diff_value_multiple
        self.seed_Minimum_density_variation = 0.05  # 种子最小密度变化,小于该值将不能成为种子,该值必须小于threshold

        self.refs_file = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\17_58MaMian_ref.den" # 参考模型
        self.start_data_file = self.refs_file  # 初始值，可为参考模型，也可以是其他反演结果，在此基础上做反演
        self.mesh_file = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\17_58MaMian.msh"  # mesh文件
        self.matrix_file = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\temp\%s"  # 矩阵等信息，反演算法的中间文件
        self.bounds_file = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\17_58MaMian_bnd.den" # 上下限
        self.moudles_file = self.refs_file  # 真实模型，可为参考模型，也可以是其他反演结果。每次将打印与该结果的差异值。如仿真中已知的结果，来评估算法的情况

    def set_start_seed(self, start_seed):
        self.start_seed = start_seed

    def set_max_count(self, max_count):
        self.max_count = max_count

    def set_out_put_dir(self, out_put_dir):
        self.out_put_dir = out_put_dir

    def set_punishment_diff_value_multiple(self, punishment_diff_value_multiple):
        self.punishment_diff_value_multiple = punishment_diff_value_multiple

    def set_punishment_Search_distancevalue_multiple(self, punishment_Search_distancevalue_multiple):
        self.punishment_Search_distancevalue_multiple = punishment_Search_distancevalue_multiple

    def set_prompt_value_multiple(self, prompt_value_multiple):
        self.prompt_value_multiple = prompt_value_multiple

    def set_misfit_all_multiple(self, misfit_all_multiple):
        self.misfit_all_multiple = misfit_all_multiple

    def set_smooth_all_multiple(self, smooth_all_multiple):
        self.smooth_all_multiple = smooth_all_multiple

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_seed_Minimum_density_variation(self, seed_Minimum_density_variation):
        self.seed_Minimum_density_variation = seed_Minimum_density_variation

    def set_refs_file(self, refs_file):
        self.refs_file = refs_file

    def set_start_data_file(self, start_data_file):
        self.start_data_file = start_data_file

    def set_mesh_file(self, mesh_file):
        self.mesh_file = mesh_file

    def set_matrix_file(self, matrix_file):
        self.matrix_file = matrix_file

    def set_bounds_file(self, bounds_file):
        self.bounds_file = bounds_file

    def set_moudles_file(self, moudles_file):
        self.moudles_file = moudles_file

    def show_arguments(self):
        myPrint_Hint("max_count=%s" % (self.max_count))
        myPrint_Hint("out_put_dir=r\"%s\"" % (self.out_put_dir))
        myPrint_Hint("punishment_diff_value_multiple=%s" % (self.punishment_diff_value_multiple))
        myPrint_Hint("punishment_Search_distancevalue_multiple=%s" % (self.punishment_Search_distancevalue_multiple))
        myPrint_Hint("prompt_value_multiple=%s" % (self.prompt_value_multiple))
        myPrint_Hint("misfit_all_multiple=%s" % (self.misfit_all_multiple))
        myPrint_Hint("smooth_all_multiple=%s" % (self.smooth_all_multiple))
        # myPrint_Hint("punishment_factor=%s"%(punishment_factor))
        myPrint_Hint("threshold=%s" % (self.threshold))
        myPrint_Hint("seed_Minimum_density_variation=%s" % (self.seed_Minimum_density_variation))
