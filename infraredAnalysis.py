import os
import pickle
import subprocess as sp
# automatically install all libraries needed.
try:
    import peakutils
except ImportError:
    while True:
        c = sp.call('pip install peakutils', shell=True)
        if c == 0:
            break
    import peakutils
try:
    import numpy as np
except ImportError:
    while True:
        c = sp.call('pip install numpy', shell=True)
        if c == 0:
            break
    import numpy as np
try:
    import pandas as pd
except ImportError:
    while True:
        c = sp.call('pip install pandas', shell=True)
        if c == 0:
            break
    import pandas as pd
try:
    import matplotlib.pyplot as plt
except ImportError:
    while True:
        c = sp.call('pip install matplotlib', shell=True)
        if c == 0:
            break
    import matplotlib.pyplot as plt


# colormap
colors = {0: 'firebrick', 1: 'pink', 2: 'saddlebrown', 3: 'darkorange', 4: 'gold', 5: 'olivedrab', 6: 'greenyellow',
          7: 'lightgreen', 8: 'plum', 9: 'Magenta', 10: 'Orchid', 11: 'Indigo', 12: 'DarkSlateBlue', 13: 'Navy',
          14: 'PowDerBlue', 15: 'Teal', 16: 'MintCream', 17: 'Lavender', 18: 'MediumBlue', 19: 'Chartreuse',
          20: 'DarkKhaki', 21: 'GoldEnrod', 22: 'BlanchedAlmond', 23: 'Tan', 24: 'IndianRed', 25: 'Gainsboro',
          26: 'Gray', 27: 'black'}

# TODO(Augus): create a neural network to identify IR peaks.


def data_open(open_file_name):
    """
    This function only deals with IR output file in csv format

    :param open_file_name: the name of csv file
    :return: a set of data that can be further used in other functions of infraredAnalysis
    """
    data_x = pd.read_csv(open_file_name, usecols=[0])
    data_y = pd.read_csv(open_file_name, usecols=[1])
    data_x = data_x.apply(pd.to_numeric, errors='coerce').fillna(0.0)
    data_y = data_y.apply(pd.to_numeric, errors='coerce').fillna(0.0)
    data_x, data_y = data_x.dropna(), data_y.dropna()
    x, y = data_x.values, data_y.values
    x, y = x.astype('float32'), y.astype('float32')
    return [x, y]


def peak_find(data, threshold=0.5, min_dist=50):
    _x, _y, x_, y_ = [], [], [], []
    x, y = data[0], data[1]
    for i in x:
        _x.append(i[0])
    for j in y:
        _y.append(100 - j[0])
    '''the above codes are used to convert data format 
    exported from Pandas into a format that can be used in PeakUtils.'''
    indexes = peakutils.indexes(np.array(_y), thres=threshold, min_dist=min_dist)
    for h in indexes:
        x_.append(_x[h])
        y_.append(100 - _y[h])
    return [np.array(x_), np.array(y_)]


def quick_peak_classify(data=None):
    """
    This function will select all peaks in the functional group range.
    Warning: this method is NOT so accurate.

    :param data: IR data exported from peak_find()
    :return: a set of classified data
    """
    address = os.getcwd() + '\\ir_peak_range_class.pkl'
    with open(address, 'rb') as f:
        peak_class = pickle.load(f)
    fre, tra = data[0], data[1]
    peak_set = {}
    for typ in peak_class:
        x_data, y_data = [], []
        a_, b_ = [[], []], [[], []]
        for key, i in enumerate(fre):
            if len(peak_class[typ]) == 1:  # peak_class[typ] = [Interval(u, d)]
                if i in peak_class[typ][0]:
                    x_data.append(i)
                    y_data.append(tra[key])
            if len(peak_class[typ]) == 2:  # peak_class[typ] = [peak_range1, peak_range2, ...]
                for key2, j in enumerate(peak_class[typ]):
                    if i in j:
                        a_[key2].append(i)
                        b_[key2].append(tra[key])
            if len(a_[0]) != 0 and len(a_[1]) != 0:
                x_data = a_[0] + a_[1]
                y_data = b_[0] + b_[1]
        if len(x_data) != 0:  # give non-empty dictionary only.
            peak_set[typ] = [x_data, y_data]
    return peak_set


def plot(set1, set2=None, title='', show=True, save=False, s_f='.jpg'):
    """
    This function is used to plot the IR spectra in a specific format.

    :param set1: the IR data exported from data_open();
    :param set2: the selected-peaks set exported from peak_find() or quick_peak_classify();
                 if set2 is None, no peak will be marked;
    :param title: the title of the plot; latex format is necessary;
    :param show: whether show the image;
    :param save: whether save the image; the image will be saved at the root file;
    :param s_f: the format of output file, e.g. '.jpg''.png''.ps''.pdf'.
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # Chinese label support.
    plt.rcParams['axes.unicode_minus'] = False  # normal 'negative symbol'
    fig = plt.figure(figsize=(20.0, 12.0))
    fig_ = fig.add_subplot(111)
    ax = fig.gca()
    ax.invert_xaxis()
    x_tick = np.arange(500, 4200, 200)
    y_tick = np.arange(0, 110, 10)
    x, y = set1[0], set1[1]
    fig_.plot(x, y, color='black', label='IR spectrum')
    if set2 is not None:
        if type(set2) is list:
            x_, y_ = set2[0], set2[1]
            fig_.scatter(x_, y_, color='orange', marker=6, s=80)
            for step, n in enumerate(x_):  # show the wave number of peaks.
                fig_.text(n, y_[step]-12, n, rotation=90, alpha=0.6, fontstyle='oblique')
        if type(set2) is dict:
            for key, typ in enumerate(set2):
                # for instance set2 = {'C=O': [x_data, y_data], 'O-H': [x_data, y_data]}
                x_ = np.array(set2[typ][0])
                y_ = np.array(set2[typ][1]) - key
                fig_.scatter(x_, y_, color=colors[key], label=typ, marker=6, s=80)
    fig_.set_xlabel(r'Wave number (cm$^{-1}$)')  # LaTex format
    fig_.set_ylabel('Transmittance (%)')
    fig_.set_xticks(x_tick), fig_.set_yticks(y_tick)
    fig_.set_title(title)  # title using LaTex format.
    fig_.grid(color='black', linestyle=':')
    fig_.legend()  # show legend
    plt.tight_layout()  # Tight-show
    figure_ = plt.get_current_fig_manager()
    try:  # full-sized the figure.
        # if backend is Qt
        figure_.resize(*figure_.window.maxsize())
    except AttributeError:
        try:
            # if backend is WX
            figure_.frame.Maximized(True)
        except AttributeError:
            # if backend is Tk
            figure_.window.showMaximized()
    finally:
        if save:
            address = os.getcwd() + '\\' + title + s_f
            plt.savefig(address, dpi=800)
        if show:
            plt.show()


def peak_data(data, out_file_name):
    """
    export peak data in a file such as a csv file.

    :param data: peak data from peak_find()
    :param out_file_name: the name of exported file, e.g. 'sample_peak.csv'
    """
    content = 'wave number,transmittance\n'
    for key, data_x in enumerate(data[0]):
        row = str(data_x) + ',' + str(data[1][key]) + '\n'
        content = content + '{}'.format(row)
    with open(out_file_name, 'w', encoding='utf-8') as f:
        f.write(content)


def batch_plot(file_root):
    """
    batch save plots.

    :param file_root: the root where wanted files exist
    """
    for root, dirs, files in os.walk(file_root):
        for name in files:
            if name.endswith('.csv') or name.endswith('.CSV'):
                a = data_open(file_root+'\\'+name)
                b = peak_find(a)
                title = name
                plot(a, b, title=title, show=False, save=True)


class Frame:
    def __init__(self, open_file_name, threshold=0.5, min_dist=50):
        self.data = data_open(open_file_name)
        self.peak = peak_find(self.data, threshold, min_dist)
        self.classify = quick_peak_classify(self.peak)

    def plot(self, title='', select=0):
        """

        :param title: the title of the plot; LaTex supported.
        :param select: select=0 -> no peaks shown;
                       select=1 -> only peaks shown;
                       select=2 -> show classified results.
        """
        if select == 0:
            plot(self.data, set2=None, title=title, show=True)
        if select == 1:
            plot(self.data, set2=self.peak, title=title, show=True)
        if select == 2:
            plot(self.data, set2=self.classify, title=title, show=True)

    def print(self, out_file_name):
        peak_data(self.peak, out_file_name)


if __name__ == '__main__':
    from time import sleep
    print('''\033[1;35mThis is a library file.
    \033[0;34m作者は　陶念澤だ。\033[0m''')
    sleep(2)
