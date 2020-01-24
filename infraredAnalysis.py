import os
import pickle
import peakutils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _open(open_file_name):
    data_x = pd.read_csv(open_file_name, usecols=[0])
    data_y = pd.read_csv(open_file_name, usecols=[1])
    data_x = data_x.dropna()
    data_y = data_y.dropna()
    x = data_x.values
    y = data_y.values
    x = x.astype('float32')
    y = y.astype('float32')
    return [x, y]


def peak_find(data, threshold=0.5, min_dist=50):
    _x = []
    _y = []
    x_ = []
    y_ = []
    x = data[0]
    y = data[1]
    for i in x:
        _x.append(i[0])
    for j in y:
        _y.append(100 - j[0])
    indexes = peakutils.indexes(np.array(_y), thres=threshold, min_dist=min_dist)
    for h in indexes:
        x_.append(_x[h])
        y_.append(100 - _y[h])
    return [np.array(x_), np.array(y_)]


def quick_peak_classify(data=None):
    # this method is not so accurate.
    address = os.getcwd() + '\\ir_peak_range_class.pkl'
    with open(address, 'rb') as f:
        peak_class = pickle.load(f)
    fre = data[0]
    tra = data[1]
    peak_set = {}
    for typ in peak_class:
        x_data = []
        y_data = []
        for key, i in enumerate(fre):
            if i in peak_class[typ]:
                x_data.append(i)
                y_data.append(tra[key])
        if len(x_data) != 0:
            peak_set[typ] = [x_data, y_data]
    return peak_set


def plot(set1, set2=None, title='', show=True, save=False):
    # set2 is the peaks set.
    color = {0: 'firebrick', 1: 'pink', 2: 'saddlebrown', 3: 'darkorange', 4: 'gold', 5: 'olivedrab', 6: 'greenyellow',
             7: 'lightgreen', 8: 'plum', 9: 'Magenta', 10: 'Orchid', 11: 'Indigo', 12: 'DarkSlateBlue', 13: 'Navy',
             14: 'PowDerBlue', 15: 'Teal', 16: 'MintCream', 17: 'Lavender', 18: 'MediumBlue', 19: 'Chartreuse',
             20: 'DarkKhaki', 21: 'GoldEnrod', 22: 'BlanchedAlmond', 23: 'Tan', 24: 'IndianRed', 25: 'Gainsboro',
             26: 'Gray', 27: 'black'}
    fig = plt.figure(figsize=(20.0, 12.0))
    fig_ = fig.add_subplot(111)
    ax = fig.gca()
    ax.invert_xaxis()
    x_tick = np.arange(500, 4200, 200)
    y_tick = np.arange(0, 110, 10)
    x = set1[0]
    y = set1[1]
    fig_.plot(x, y, color='black', label='IR spectrum')
    if set2 is not None:
        if type(set2) is list:
            x_ = set2[0]
            y_ = set2[1]
            fig_.scatter(x_, y_, color='orange', marker=6, s=80)
        if type(set2) is dict:
            for key, typ in enumerate(set2):
                # for instance set2 = {'C=O': [x_data, y_data], 'O-H': [x_data, y_data]}
                x_ = np.array(set2[typ][0])
                y_ = np.array(set2[typ][1]) - key
                fig_.scatter(x_, y_, color=color[key], label=typ, marker=6, s=80)
    fig_.set_xlabel(r'Wave number (cm$^{-1}$)')  # LaTex
    fig_.set_ylabel('Transmittance (%)')
    fig_.set_xticks(x_tick), fig_.set_yticks(y_tick)
    fig_.set_title(title)  # title using LaTex.
    fig_.grid(color='black', linestyle=':')
    fig_.legend()
    figure_ = plt.get_current_fig_manager()
    try:
        figure_.resize(*figure_.window.maxsize())
    except AttributeError:
        try:
            figure_.frame.Maximized(True)
        except AttributeError:
            figure_.window.showMaximized()
    finally:
        if save:
            address = os.getcwd() + '\\' + title + '.png'
            plt.savefig(address, dpi=500)
        if show:
            plt.show()


def peak_data(data, out_file_name):
    content = 'wave number,transmittance\n'
    for key, data_x in enumerate(data[0]):
        row = str(data_x) + ',' + str(data[1][key]) + '\n'
        content = content + '{}'.format(row)
    with open(out_file_name, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    print('''\033[1;35mThis is a library file\033[0m
          作者は　陶念澤だ。''')
