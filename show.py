"""
给定数据和分段信息，绘制分段曲线
"""
"""
给定数据和分段信息，绘制分段曲线
"""

import file_test
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pymongo
import os
import numpy as np

def draw(datafile, database, errornumber):
    data_1 = file_test.open_excel(datafile)  # 读取数据文件
    data = file_test.preprocess(data_1)
    for key in data.keys():
        preprocess(data, datafile, database, key, errornumber)



def preprocess(data, datafile, database, key, errornumber):
    client = MongoClient()  # 读取数据库文件
    db = client[database]
    col = db[key]

    ''' 计算y1, x'''
    y1 = data[key]
    length = len(y1)
    x = [i + 1 for i in range(length)]
    y2 = []
    k = []
    b = []
    length = []
    start = []

    for doc in col.find({'errornumber': errornumber}):
        k.append(doc['k'])
        b.append(doc['b'])
        length.append(doc['len'])
        start.append(doc['window_start'])
    for i in range(len(length)):
        first = length[i]
        y_2 = [k[i] * j + b[i] for j in range(first)]  # 单个输出不加，连续输出要加+start[i]
        y2 += y_2
    # print(y2)
    """防止遗漏，补位"""
    # dif = len(x) - len(y2)
    # for i in range(dif):
    #     y2.append(0)
    y = np.array(y1)
    plt.rcParams['figure.figsize'] = (40, 24)  # 设置figure_size尺寸
    plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    # print(len(y), len(y2))
    plt.plot(y, color="orange", label="Fitting Line", linewidth=1)
    plt.plot(y2, color="black", label="Fitting Line", linewidth=1)
    plt.savefig('X:\\研二\\图片\\{}\\{}.jpg'.format(errornumber, key))
    plt.cla()
    # plt.show()


def input(datafile, database='test2', errornumber='0'):
    try:
        os.mkdir('X:\\研二\\图片\\{}'.format(errornumber))
    except:
        pass
    draw(datafile, database, errornumber)


