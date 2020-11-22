# 通过index参数设置行索引，通过columns参数设置列索引
import pandas as pd
import numpy as np

# 通过index参数设置行索引，通过columns参数设置列索引
import pandas as pd
import numpy as np
import pickle


def preprocess(data):
    """将 Dataframe得数据处理为词典类型"""
    keys = list(data.keys())
    data_dic = {}
    for key in keys:
        data_dic[key] = list(data[key])  # 将所有的数据按照参数以列表的形式存储在词典中
    return data_dic


def write_excel(self):
    with open(self.filename, 'w') as file_object:
        for i in self.data:
            file_object.write(str(i) + '\n')


def read_excel(filename):
    content = []
    with open(filename, 'r') as file_object:
        for line in file_object.readlines():
            content.append(float(line))
    return content


def open_excel(filename):  # 打开相应的excel文件
    if filename[-4:] == 'xlsx':
        data = pd.read_excel(filename)
    else:
        data = pd.read_csv(filename)
    return data


def open_pickle(filename):
    file = open(filename, 'rb')
    data = pickle.load(file)
    return data
