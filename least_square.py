import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


def cal_error(y, k, b):  # 根据拟合的直线，计算数据与直线之间的差值
    node_nunber = len(y)
    error = 0
    for i in range(node_nunber):
        error += abs(y[i] - (k * i + b))
    return error


def lost_func(x, y, k, b,errornumber):
    maxerr = 0
    length = len(x)
    for i in range(length):
        maxerr += abs((k * x[i] + b) * 0.1 * (0.9 ** i))
    return maxerr if maxerr > errornumber else errornumber


def error(p, x, y):  # 拟合方程误差函数
    return (p[0] * x + p[1]) - y


def cal(xi, yi,errornumber):  # 拟合函数
    p0 = [2, 2]
    Para = leastsq(error, p0, args=(xi, yi))
    k = Para[0][0]  # 拟合得到的k, b
    b = Para[0][1]
    errors = cal_error(yi, k, b)  # 总误差

    max_lost = lost_func(xi, yi, k, b,errornumber)

    if errors > max_lost:  #
        suitable = False
    else:
        suitable = True

    #
    # plt.scatter(xi, yi, color="red", label="Sample Point", linewidth=3)
    # y=k*xi+b
    # plt.plot(xi,y,color="orange",label="Fitting Line",linewidth=2)
    # plt.show()
    return errors, k, b, suitable
