def input(info):
    keys = info.keys()
    error = {}
    sum = 1
    for key in keys:
        win_num = len(info[key])
        error[key] = 0
        for i in range(win_num):
            error[key] += info[key][i]['error']
        sum *= error[key]
    return sum, win_num