# @Time    : 2024/9/4 21:51
# @Author  : denghl1
# @Site    : 
# @File    : auto_seed.py
# @Software: PyCharm


import os

import pandas as pd
from tqdm import tqdm

from InvDataTools import Cell_Weight_Tools
from InvDataTools import Gij_tools
from InvDataTools import Jxyz_Tools
from InvDataTools import MeshTools
from InvDataTools import obs_tools
from InvDataTools import ref_tools
from InvDataTools.calculate import Calcu_sensitivity


def get_neighbor_js(j, shape, distance):
    """

    :param j:
    :param shape:
    :param distance: 周围几个体素，平滑的距离
    :return:找的附近几个体素的编号
    """

    if shape is None:
        shape = [2, 5, 8]
    x, y, z = Jxyz_Tools.getxyz_from_shape(shape, j)
    res = set()

    # 周围(2N)**3个
    for xx in range(x - distance, x + distance + 1):
        if xx < 0 or xx >= shape[0]:
            continue
        for yy in range(y - distance, y + distance + 1):
            if yy < 0 or yy >= shape[1]:
                continue
            for zz in range(z - distance, z + distance + 1):
                if zz < 0 or zz >= shape[2]:
                    continue
                res.add(Jxyz_Tools.getj_from_xyz(shape, (xx, yy, zz)))
    return res


def select_rays(sig_threads: dict, obs_path, abnormal_obs_path_high, abnormal_obs_path_small):
    """

    :param sig_threads:
    :param obs_path:
    :param abnormal_obs_path_high:
    :param abnormal_obs_path_small:
    :return: 异常射线文件生成
    """
    df = pd.read_csv(obs_path, sep='\s+')
    grouped = df.groupby(by='DetID')
    result_df = pd.DataFrame(columns=df.columns)
    for name, per_det_df in grouped:
        per_det_df = per_det_df[per_det_df['SmoothSig'] > sig_threads[name]]
        result_df = pd.concat([result_df.copy(), per_det_df.copy()], ignore_index=None)

    result_df.to_csv(abnormal_obs_path_high, index=None, sep=' ')

    result_df = pd.DataFrame(columns=df.columns)
    for name, per_det_df in grouped:
        per_det_df = per_det_df[per_det_df['SmoothSig'] < -sig_threads[name]]
        result_df = pd.concat([result_df.copy(), per_det_df.copy()], ignore_index=None)
    result_df.to_csv(abnormal_obs_path_small, index=None, sep=' ')
    print('异常射线挑选完毕')


def get_abnormal_cells_by_rays_1(d_path, g_path, gij_path, ray_way_j_path, res_dir, abnormal_obs_path_high,
                                 all_obs_path, ref_path, msh_path,
                                 min_rays_num, detectors_num, abnormal_per, neighbour_distance,
                                 abnormal_neighbour_thread, begin_point=None, end_point=None):
    """
    找种子，射线交点
    :param end_point: 需要求的范围，如地堡只需要马面部分，其余部分相交也去除不作为种子，减少计算seed算法,传入的连续的xyz坐标
    :param begin_point:
    :param abnormal_obs_path_high:
    :param d_path:
    :param g_path:
    :param neighbour_distance:
    :param abnormal_neighbour_thread:
    :param gij_path:
    :param ray_way_j_path:
    :param res_dir:
    :param all_obs_path:
    :param ref_path:
    :param msh_path:
    :param min_rays_num:
    :param detectors_num:
    :param abnormal_per:
    :return:生成种子文件
    """
    msh_obj = MeshTools.MeshTools(msh_path)
    ref_dens = ref_tools.Ref_tools(ref_path).get_data()
    dis_begin = None
    dis_end = None
    if begin_point:
        dis_begin = msh_obj.discretize_Physical_coordinates(begin_point[0], begin_point[1], begin_point[2])
        dis_end = msh_obj.discretize_Physical_coordinates(end_point[0], end_point[1], end_point[2])
    print(f"种子范围在{dis_begin}~{dis_end},计算正常射线经过的体素")
    calc_sensitivity_obj = Calcu_sensitivity.Calcsensitivity(mesh_tool=msh_obj, obs_file=abnormal_obs_path_high)
    calc_sensitivity_obj.calc_all_rays_from_obs_file(gij_path, ray_way_j_path)
    ray_way_js: list = Cell_Weight_Tools.Cell_Weight_Tools(ray_way_j_path).data
    detectors_id = [i[0] for i in obs_tools.obs_tools(abnormal_obs_path_high).get_data()]
    rays_num = [0] * msh_obj.cells_count()  # 穿过体素的不正常射线数量
    detectors_sets = [set() for _ in range(msh_obj.cells_count())]
    for index, cells_id in enumerate(ray_way_js):  # index第几条射线，从0开始；cells_id表示第几个体素，从1开始
        det_id = detectors_id[index]
        for cell_id in cells_id:
            rays_num[cell_id - 1] += 1
            detectors_sets[cell_id - 1].add(det_id)
    if abnormal_per > 0:
        print("计算所有射线经过的体素")
        calc_sensitivity_all_obj = Calcu_sensitivity.Calcsensitivity(mesh_tool=msh_obj, obs_file=all_obs_path)
        calc_sensitivity_all_obj.calc_all_rays_from_obs_file(gij_path, ray_way_j_path)
        Gij_tools.get_g(gij_path, g_path)  # 生成G文件，虽然这里没有，但是seed算法需要
        ray_way_js_all: list = Cell_Weight_Tools.Cell_Weight_Tools(ray_way_j_path).data
        all_ray_num = [0 for _ in range(msh_obj.cells_count())]
        with open(d_path, 'w') as f:  # seed算法要用
            obs_obj = obs_tools.obs_tools(all_obs_path)
            ds = obs_obj.get_d_form_obs()
            abs_errs = obs_obj.get_d_absolute_err_form_obs()
            for d, abs_err in zip(ds, abs_errs):
                f.write(f"{d} {abs_err}\n")
        for index, cells_id in enumerate(ray_way_js_all):  # index第几条射线，从0开始；cells_id表示第几个体素，从1开始
            for cell_id in cells_id:
                all_ray_num[cell_id - 1] += 1
        print("计算异常体素")
        for index, detectors_set in enumerate(detectors_sets):
            if len(detectors_set) < detectors_num or ref_dens[index] == 0 or rays_num[index] < min_rays_num or (
                    rays_num[index] / all_ray_num[index] < abnormal_per / 100):
                rays_num[index] = 0
    else:
        for index, detectors_set in enumerate(detectors_sets):
            if len(detectors_set) < detectors_num or ref_dens[index] == 0 or rays_num[index] < min_rays_num:
                rays_num[index] = 0
    smooth_result = rays_num.copy()
    result_js = set()
    for i in tqdm(range(len(rays_num)), desc="smoothing"):
        if smooth_result[i] > 0:
            neighbor_num = 0
            js = get_neighbor_js(i + 1, msh_obj.get_shape(), neighbour_distance)
            for j in js:
                if rays_num[j - 1] > 0:
                    neighbor_num += 1
            if neighbor_num < abnormal_neighbour_thread:
                smooth_result[i] = 0
            else:
                xyz = Jxyz_Tools.getxyz_from_shape(msh_obj.get_shape(), i + 1)
                if not dis_begin:  # 是否有
                    result_js.add(i + 1)
                else:
                    if dis_begin[0] <= xyz[0] and dis_begin[1] <= xyz[1] and dis_begin[2] <= xyz[2] and dis_end[0] >= \
                            xyz[0] and dis_end[1] > xyz[1] and dis_end[2] > xyz[2]:
                        result_js.add(i + 1)
    # if model:  # 1终端，需要写文件
    print(fr"终端写文件 {res_dir}")
    with open(fr"{res_dir}\ray{min_rays_num}det{detectors_num}_per{abnormal_per}.den", 'w') as f:
        f.write("\n".join([str(_) for _ in rays_num]))
    with open(rf"{res_dir}\smooth.den", 'w') as f:
        f.write("\n".join([str(_) for _ in smooth_result]))
    with open(rf"{res_dir}\seed_js.txt", 'w') as f:
        f.write("\n".join([str(_) for _ in result_js]))
    # return rays_num, smooth_result, result_js


def run():
    # 输入参数，下面参数需要修改
    sig_dic = {1: 3, 2: 3, 3: 3, 4: 2, 5: 2, 6: 2}  # 探测器的sig
    model = 1  # 是否生成文件 0不生1生成

    # 后面参数使用默认不变即可
    min_rays_num = 2  # 射线数量
    detectors_num = 2  # 探测器数量
    percent = 40  # 异常射线百分比， 设置为负数就不会算所有的射线了，会特别快，但是无法去除靠近探测器的区域可能会有异常大片
    neighbour_distance = 4  # 平滑时周围搜索的距离
    abnormal_neighbour_thread = 30  # 异常体素数量阈值

    # 输入文件
    gij_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\temp\Gij"
    d_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\temp\d"
    g_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\temp\G"
    assist_j_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\temp\Assist_j"
    jxyz_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\temp\jxyz"
    ray_way_j_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\temp\Ray_way_j"
    obs_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\total_ray.dat"
    msh_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\17_58MaMian.msh"
    ref_path = r"E:\vscode\Muon_Imaging_Algorithm\data\paper3\wall\17_58MaMian_ref.den"

    #  输出文件路径
    res_dir = os.path.join(os.path.dirname(ref_path), 'abnormal_space')
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    abnormal_obs_path_high = os.path.join(res_dir, 'sig_larger.dat')
    abnormal_obs_path_small = os.path.join(res_dir, 'sig_small.dat')

    # 执行代码
    select_rays(sig_dic, obs_path, abnormal_obs_path_high, abnormal_obs_path_small)
    get_abnormal_cells_by_rays_1(d_path,
                                 g_path,
                                 gij_path,
                                 ray_way_j_path,
                                 res_dir,
                                 abnormal_obs_path_high,
                                 obs_path,
                                 ref_path,
                                 msh_path,
                                 min_rays_num, detectors_num, percent, neighbour_distance, abnormal_neighbour_thread,
                                 )


def get_js_in_specified_range(begin_point, end_point, msh_obj: MeshTools.MeshTools):
    dis_begin = msh_obj.discretize_Physical_coordinates(begin_point[0], begin_point[1], begin_point[2])
    dis_end = msh_obj.discretize_Physical_coordinates(end_point[0], end_point[1], end_point[2])
    result_js = []
    for dis_x in range(dis_begin[0], dis_end[0] + 1):
        for dis_y in range(dis_begin[1], dis_end[1] + 1):
            for dis_z in range(dis_begin[2], dis_end[2] + 1):
                j = Jxyz_Tools.getj_from_xyz(msh_obj.get_shape(), (dis_x, dis_y, dis_z))
                result_js.append(j)
    return result_js


def make_temp_file(msh_path, obs_path, gij_path, g_path, d_path, ray_way_j_path):
    msh_obj = MeshTools.MeshTools(msh_path)
    calc_sensitivity_obj = Calcu_sensitivity.Calcsensitivity(mesh_tool=msh_obj, obs_file=obs_path)
    calc_sensitivity_obj.calc_all_rays_from_obs_file(gij_path, ray_way_j_path)
    Gij_tools.get_g(gij_path, g_path)  # 生成G文件，虽然这里没有，但是seed算法需要
    with open(d_path, 'w') as f:
        obs_obj = obs_tools.obs_tools(obs_path)
        ds = obs_obj.get_d_form_obs()
        abs_errs = obs_obj.get_d_absolute_err_form_obs()
        for d, abs_err in zip(ds, abs_errs):
            f.write(f"{d} {abs_err}\n")

# print(get_js_in_specified_range((-2.5, -2.5, 21.2), (2.5, 2.5, 26.2), MeshTools.MeshTools(r"E:\data\jy\jy.msh")))
# run()
