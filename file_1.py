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
import parameter


def cal_st(datalist, st, t, a):  # 计算下一步的st, 判断是否在现在的节点进行分段
    y = 0
    s = 0
    for i in range(0, t):
        y += (1 - a) ** i * datalist[t - i - 1]
    out = y * a + (1 - a) ** t * st[0]
    return out


def measure(seg_list,errornumber):  # 判断当前的分段是否满足先行分段表示的约束

    lens = len(seg_list)
    X = []
    Y = []
    for i in range(lens):
        X.append(i)
        Y.append(seg_list[i])
    Xi = np.array(X)
    Yi = np.array(Y)
    error, k, b, suitable = least_square.cal(Xi, Yi,errornumber)
    return error, k, b, suitable


class St():
    def __init__(self, data, st, a, p):
        self.data = data        # 数据串
        self.st = st    # 预测值
        self.a = a      # smoothing coefficient
        self.p = p      # compression

    def cal_st(self):
        """ 根据之前的实际值和预测值，计算得出当前位置的预测值"""
        true_value = self.data[-2]     # 已经确定的真实值是除去最后一个的数组
        predict_value = self.st         # 之前预测的值
        new_predict_value = a*true_value+(1-a)*predict_value
        return new_predict_value

    def cal_err(self, V, new_predict_value):
        """ 计算的当前位置的误差值，并将其加入到预测数组中"""
        V.append(abs(self.data[-1]-new_predict_value))
        errors = np.array(V)
        Mu = np.mean(errors)
        Sigma = np.std(errors)
        sat = True
        if V[-1] > Mu-ratio*Sigma or V[-1] < Mu-ratio*Sigma:
            sat = False
        return V, sat

    # def collect(self, SKPS, SegNum, RErrSum):
    #     SKPS.append(i)
    #     SegNum += 1




def engine(series, a, filename,errornumber):
    keys = list(series.keys())
    length = series.index.shape[0]  # 时序数据的长度
    data_dic = {}
    seg_list = {}
    st = {}

    '''窗口参数初始化'''
    windows_number = 1  # 目前是第几个窗口
    windows = {}  # 记录窗口的信息
    window_len = 2  # 当前窗口的长度
    window_start = 0  # 当前窗口的开始位置、
    window_end = 1  # 当前窗口的结束位置
    store_win_info = {}
    for key in keys:
        data_dic[key] = list(series[key])  # 将所有的数据按照参数以列表的形式存储在词典中
        seg_list[key] = [data_dic[key][0]]
        st[key] = [data_dic[key][0]]  # 利用初始值初始化st
        windows[key] = []
        store_win_info[key] = {}
    '''线性近似初始化'''
    error, k, b = 0, 0, 0
    judge_st = True
    judge_linear = True

    while True:
        assert window_end > window_start
        assert window_len == (window_end - window_start + 1)

        """窗口滑动, 如果已经到了结尾则直接停止并输出，否则设置一个临时词典存储"""
        if window_end == length - 1:
            for key in keys:
                seg_list[key] = data_dic[key][window_start:]  # 切片添加当前位置的数据
                error, k, b, suitable = measure(seg_list[key],errornumber)  # 计算拟合参数
                windows[key].append(
                    {'number': windows_number, 'error': error, 'k': k, 'b': b, 'window_start': window_start,
                     'len': window_len, 'file': filename})  # 保存当前分段的信息
            break
        else:
            for key in keys:
                seg_list[key] = data_dic[key][window_start: window_end + 1]  # 切片添加当前位置的数据
                if window_len <= 2:         # 小于等于2的分段先初始化， 做好信息备份
                    error, k, b, suitable = measure(seg_list[key],errornumber)
                    store_win_info[key] = {'number': windows_number, 'error': error, 'k': k, 'b': b,
                                           'window_start': window_start,
                                           'len': window_len, 'file': filename}  # 如果只有两个数据时先计算暂时的分段信息，也就是初始化

        """ 判定的第一部分， 利用st进行指数预测"""
        store_st = []
        store_V = []
        if len(seg_list ==1 ):
            pass
        else:
            for key in keys:
                judger = St(seg_list[key],st[key],a,p)
                st_value = judger.cal_st()
                V, judge_st = judger.cal_err(V, st_value)
                store_st.append(st_value)
                store_V.append(V)
                if judge_st == False: break
        if judge_st:
            for i in range(len(keys)):
                st[keys[i]].append(store_st[i])
                V[keys[i]].append(store_V[i])


        """ 判定的第二部分， 利用PLA进行误差约束"""

        if judge_st:  # 如果st满足再进行线性拟合
            for key in keys:
                x_1, x_2, x_3, judge_linear = measure(seg_list[key],errornumber)
                if not judge_linear:  # 测试写一个点分段是否满足约束, 不满足则跳转
                    break
                else:

                    """ 经过前边所有的检测之后符合条件则计算分段信息，判断后更新作为截至之前的备份 """
                    error, k, b = x_1, x_2, x_3  # 如果当前数据满足条件则更新数据， 如果不满足则沿用上一个的数据
                    store_win_info[key] = {'number': windows_number, 'error': error, 'k': k, 'b': b,
                                           'window_start': window_start, 'file': filename}

        """ 在这里设置分段长度。前边是不符既跳的结构，会造成长度不一"""
        if judge_linear and judge_st:
            for key in keys:
                store_win_info[key]['len'] = window_len
        else:
            for key in keys:
                store_win_info[key]['len'] = window_len - 1

        """ 根据上述的判断条件，决定是否在当前节点后进行分段，如果分段，将当前分段的信息存储在Windows中，并进行下一个窗口的划动"""
        if not judge_linear or not judge_st:  # 如果下一个数据不满足条件则并指拓展并初始化参数
            for key in keys:
                windows[key].append(store_win_info[key])  # 把对应的变量的分段信息存储进来--> {'IA':[], 'IB':[]..}
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
    p = 0  # compression rate
    a = 0.2  # smoothing coefficient
    V = []  # predicted error
    ratio = 0  # determine by p

    '''output'''
    SKPS = []  # Segmenting Key Points Set
    RErrSum = 0  # total residual error

    winerror = []
    winnum = []
    for err in tqdm(range(0, 1000, 20)):


        filename = 'new.xlsx'
        database = 'test1'
        errornumber = err

        series = file_rw.open_excel(filename)
        windows = engine(series, a, filename,errornumber,)  # 返回窗口信息
        x1, x2 = parameter.input(windows)
        winerror.append(x1)
        winnum.append(x2)

        mongo.input(windows, database, errornumber)
        show.input(filename, database, errornumber)


    print(winerror, winnum)
    filename = 'programming.txt'
    file_rw.write_excel(winerror, 'error.txt')
    file_rw.write_excel(winnum, 'number.txt')

    x = [i + 1 for i in range(len(winnum))]

    # plt.rcParams['figure.figsize'] = (40, 24)  # 设置figure_size尺寸
    # plt.plot(x, winnum, color="orange", label="Fitting Line", linewidth=1)
    #
    # plt.plot(x, winerror, color="black", label="Fitting Line", linewidth=1)
    # plt.savefig('1.jpg')
    # plt.show()
