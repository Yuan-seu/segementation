import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq
import least_square
from tqdm import tqdm
from tqdm._tqdm import trange
import file_rw
import ex_pre
import show
import mongo


def cal_st(datalist, st, t,a):  # 计算下一步的st, 判断是否在现在的节点进行分段
    y=0
    s=0
    for i in range(0,t):
        y+=(1-a)**i*datalist[t-i-1]
    out = y*a+(1-a)**t*st[0]
    return out

def measure(seg_list):  # 判断当前的分段是否满足先行分段表示的约束

    lens = len(seg_list)
    X = []
    Y = []
    for i in range(lens):
        X.append(i)
        Y.append(seg_list[i])
    Xi = np.array(X)
    Yi = np.array(Y)
    error, k, b, suitable = least_square.cal(Xi, Yi)
    return error, k, b, suitable


def engine(data, length,a ):
    keys = list(series.keys())
    data_dic = {}
    seg_list = {}
    st = {}

    '''窗口参数初始化'''
    windows_number = 1      # 目前是第几个窗口
    windows = {}            # 记录窗口的信息
    window_len = 2          # 当前窗口的长度
    window_start = 0        # 当前窗口的开始位置、
    window_end = 1          # 当前窗口的结束位置
    store_win_info = {}
    #tem_info ={}
    for key in keys:
        data_dic[key] = list(series[key])  # 将所有的数据按照参数以列表的形式存储在词典中
        seg_list[key] = [data_dic[key][0]]
        st[key] = [data_dic[key][0]]  # 利用初始值初始化st
        windows[key] = []
        store_win_info[key] = {}
        #tem_info[key]= {}
    print(st)
    '''线性近似初始化'''
    error, k, b = 0, 0, 0
    judge_st = True
    judge_linear = True

    while True:
        assert window_end > window_start
        assert window_len == (window_end - window_start + 1)


        """窗口滑动"""
        if window_end == length - 1:
            for key in keys:
                seg_list[key] = data_dic[key][window_start: ]  # 切片添加当前位置的数据
                error, k, b, suitable = measure(seg_list[key])          # 计算拟合参数
                windows[key].append({'number': windows_number, 'error': error, 'k': k, 'b': b, 'window_start': window_start,
                                       'len': window_len, })  # 保存当前分段的信息
            break
        else:
            for key in keys:
                seg_list[key] = data_dic[key][window_start: window_end+1]  # 切片添加当前位置的数据
                if window_len <=2:
                    error, k, b, suitable = measure(seg_list[key])
                    store_win_info[key] = {'number': windows_number, 'error': error, 'k': k, 'b': b,
                                           'window_start': window_start,
                                           'len': window_len }  # 如果只有两个数据时先计算暂时的分段信息，也就是初始化

                """ 判定的第一部分， 利用st进行指数预测"""
                # new_st = cal_st(data_dic[key], st[key], window_end,a)
                # st[key].append(new_st)  # 计算下一步的st, 判断是否在现在的节点进行分段
                # if not ex_pre.inrange(data_dic[key], st[key],new_st):     # 如果指数预测不符合，则直接输出
                #     judge_st = False
                #     error, x_2, x_3, judge_linear = measure(seg_list[key])

        """ 判定的第二部分， 利用PLA进行误差约束"""

        if judge_st:        # 如果st满足再进行线性拟合
            for key in keys:
                x_1, x_2, x_3, judge_linear = measure(seg_list[key])

                if not judge_linear or not judge_st:  # 测试写一个点分段是否满足约束, 不满足则跳转
                    break
                else:
                    error, k, b = x_1, x_2, x_3  # 如果当前数据满足条件则更新数据， 如果不满足则沿用上一个的数据
                    # tem_info[key] = {'number': windows_number, 'error': error, 'k': k, 'b': b,
                    #                        'window_start': window_start,
                    #                        'len': window_len}  # 如果只有两个数据时先计算暂时的分段信息，也就是初始化
                    store_win_info[key] = {'number': windows_number, 'error': error, 'k': k, 'b': b,
                                           'window_start': window_start }  # 如果只有两个数据时先计算暂时的分段信息，也就是初始化
        if judge_linear:
            for key in keys:
                store_win_info[key]['len'] = window_len
        else:
            for key in keys:
                store_win_info[key]['len'] = window_len-1

        """ 根据上述的判断条件，决定是否在当前节点后进行分段，如果分段，将当前分段的信息存储在Windows中，并进行下一个窗口的划动"""
        if not judge_linear or not judge_st:  # 如果下一个数据不满足条件则并指拓展并初始化参数
            for key in keys:
                windows[key].append(store_win_info[key])        # 把对应的变量的分段信息存储进来--> {'IA':[], 'IB':[]..}
                seg_list[key] = []
            windows_number += 1
            judge_st = True  # 对参数进行刷新
            judge_linear = True
            window_start = window_end  # 下一个窗口的起始位置
            window_end = window_end + 1  # 下一个窗口的起始位置
            window_len = 2  # 如何不从一开始

        else:
            window_len += 1  # 扩大窗口
            window_end += 1
    return windows

if __name__ == '__main__':
    '''初始化设置'''
    # p = 0  # compression rate
    # TraningSize = 0  # size of training set
    a = 0.2  # smoothing coefficient
    # V = []  # predicted error
    # ratio = 0  # determine by p
    # '''output'''
    # SKPS = []  # Segmenting Key Points Set
    # RErrSum = 0  # total residual error

    # filename = 'F:\\研二数据\\数据\\接触器\\1-\\ndc1-3810\\1#ToExcel\\2020年08月26日13时38分37.27秒 第1次.xlsx'
    filename = 'new.xlsx'
    series = file_rw.open_excel(filename)
    TraningSize = series.index.shape[0]  # 时序数据的长度
    windows = engine(series, TraningSize,a)
    data = []
    mongo.input(windows)

