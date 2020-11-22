from tqdm import tqdm
import pandas as pd
import least_square
import numpy as np
import re
import file_rw
import show
import matplotlib.pyplot as plt

# def write_excel(filename, data):
#     frame = pd.DataFrame(data)
#     frame.to_excel(filename, index= False)
#     # with open(filename, 'w') as file_object:
#     #     for i in data:
#     #         file_object.write(str(i) + '\n')
# file = file_rw.FileOperation( 'arcing_ftr_dict.pkl')
# data = file.open_pickle()
# keys = data.keys()
# for key in keys:
#     write_excel(key+'.xlsx', data[key])
#


# x=[0.295,-0.528,0.245,-0.502,0.029,-0.426,0.422,1.548,-0.515]
# y=[1,2,3,4,5,6,7,8,9]
#
# filename = 'programming.txt'
# with open(filename, 'w') as file_object:
#     for i in x:
#         file_object.write(str(i)+'\n')
# filename = 'programming.txt'
# content = []
# with open(filename, 'r') as file_object:
#     for line in file_object.readlines():
#         content.append(float(line))
# print(content)
#
# # print(least_square.cal(np.array(y),np.array(x)))


def read_excel(filename):
    content = []
    with open(filename, 'r') as file_object:
        for line in file_object.readlines():
            content.append(float(line))
    # print(content)
    return content

error = read_excel('error.txt')
number = read_excel('number.txt')
# show.input(error,number)
error= [(i-min(error))/(max(error)-min(error)) for i in error]
number= [(i-min(number))/(max(number)-min(number)) for i in number]
multi = [error[i]*number[i] for i in range(len(error))]
multi =[(i-min(multi))/(max(multi)-min(multi)) for i in multi]


length = len(error)
x = [i + 1 for i in range(length)]
print([(number[i] - error[i]) for i in range(len(number))])
plt.rcParams['figure.figsize'] = (40,24)  # 设置figure_size尺寸
# plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
plt.plot(x, error,color="orange",label="Fitting Line",linewidth=10)

plt.plot(x, number, color="black", label="Fitting Line", linewidth=10)
plt.plot(x, multi, color="red", label="Fitting Line", linewidth=1)
# plt.savefig('X:\\研二\\图片\\{}\\{}.jpg'.format(errornumber,key))
plt.show()

# filename = 'datafile.xlsx'
# file_read = file_rw.FileOperation(filename)
# database = 'test4'
# series = file_read.open_excel()
# old = series
# print(old)
# # for key in series.keys():
# # series[key] = series[key][6225: 6352]
# y1 = old['IA']
# # y2 = np.array(series[key])
# # print(type(y2))
# # a = np.zeros(6225)
# # b = np.zeros(3048)
# # y2 = list(y2)
# # a = list(a)
# # b = list(b)
# # y2 = a+y2+b
# x =
#
# data = pd.read_excel('datafile.xlsx')
# for key in data.keys():
#     plt.rcParams['figure.figsize'] = (40, 24)  # 设置figure_size尺寸
#     plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
#     plt.plot(np.array(data[key]), color="orange", label="Fitting Line", linewidth=10)
#     # plt.plot(y2, color="black", label="Fitting Line", linewidth=1)
#     plt.savefig('{}-2.jpg'.format(key))
#     plt.show()

#
# filename = 'datafile.xlsx'
#     file_read = file_rw.FileOperation(filename)
#     database = 'test4'
#     series = file_read.open_excel()
#     old = series
#     for key in series.keys():
#
#         y1 = old[key]
#         y2 = np.zeros(9600)
#         print(y2.shape)
#         for i in range(len(y1)):
#             if i < 6225 or i > 6352:
#                 y2[i] = 0
#             else:
#                 y2[i] = series[key][i]
#         plt.rcParams['figure.figsize'] = (40, 24)  # 设置figure_size尺寸
#         plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
#         plt.plot(y1, color="orange", label="Fitting Line", linewidth=1)
#         plt.plot(y2, color="black", label="Fitting Line", linewidth=1)
#         plt.savefig('{}.jpg'.format(key))
#         plt.show()
#         plt.cla()
#
# filename = 'datafile.xlsx'
# file_read = file_rw.FileOperation(filename)
# database = 'test4'
# series = file_read.open_excel()
# rh_data = {}
# for key in series.keys():
#     y2 = np.zeros(len(series[key]))
#     for i in range(len(y2)):
#         if i < 6225 or i > 6352:
#             y2[i] = 0
#         else:
#             y2[i] = series[key][i]
#     rh_data[key] = y2[6225:6353]
#
# rh_data = pd.DataFrame(rh_data)
# print(rh_data)
# rh_data.to_excel('rhdata.xlsx', index=False)


