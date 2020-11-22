import numpy as np


def cal_abs_err(data, st):
    abs_err = []
    length = min(len(data), len(st))
    for i in range(length):
        abs_err.append(abs(data[i]-st[i]))
    return abs_err,length

def cal_nor_para(abs_err,length):
    err = np.array(abs_err)
    mu = np.mean(err)
    o = (np.mean((err-mu)**2))**0.5
    return  mu, o       # 返回均值方差

def inrange(data, st, new_st):
    abs_err,length = cal_abs_err(data, st)
    mu, o = cal_nor_para(abs_err,length)
    if abs(new_st-mu) < 0*2:
        return True
    else:
        False