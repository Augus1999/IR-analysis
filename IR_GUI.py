# author@Augus
import matplotlib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from infraredAnalysis import *


def _plot(set1, set2=None, title=''):
    # set2 is the selected peaks set.
    colors = {0: 'firebrick', 1: 'pink', 2: 'saddlebrown', 3: 'darkorange', 4: 'gold', 5: 'olivedrab', 6: 'greenyellow',
              7: 'lightgreen', 8: 'plum', 9: 'Magenta', 10: 'Orchid', 11: 'Indigo', 12: 'DarkSlateBlue', 13: 'Navy',
              14: 'PowDerBlue', 15: 'Teal', 16: 'MintCream', 17: 'Lavender', 18: 'MediumBlue', 19: 'Chartreuse',
              20: 'DarkKhaki', 21: 'GoldEnrod', 22: 'BlanchedAlmond', 23: 'Tan', 24: 'IndianRed', 25: 'Gainsboro',
              26: 'Gray', 27: 'black'}
    fig = Figure(figsize=(8.0, 5.0))
    fig_ = fig.add_subplot(111)
    ax = fig.gca()
    ax.invert_xaxis()
    x_tick = np.arange(500, 4200, 200)
    y_tick = np.arange(0, 110, 10)
    x = set1[0]
    y = set1[1]
    fig_.plot(x, y, color='black', label='IR spectrum', linewidth=0.8)
    if set2 is not None:
        if type(set2) is list:
            x_ = set2[0]
            y_ = set2[1]
            fig_.scatter(x_, y_, color='orange', marker=6, s=30)
            for step, n in enumerate(x_):  # show the wave number of peaks.
                fig_.text(n, y_[step]-14, n, rotation=90, alpha=0.6, fontsize=8, fontstyle='oblique')
        if type(set2) is dict:
            for key, typ in enumerate(set2):
                # for instance set2 = {'C=O': [x_data, y_data], 'O-H': [x_data, y_data]}
                x_ = np.array(set2[typ][0])
                y_ = np.array(set2[typ][1]) - key
                fig_.scatter(x_, y_, color=colors[key], label=typ, marker=6, s=30)
    fig_.set_xlabel(r'Wave number (cm$^{-1}$)')  # LaTex
    fig_.set_ylabel('Transmittance (%)')
    fig_.set_xticks(x_tick), fig_.set_yticks(y_tick)
    fig_.tick_params(labelsize=8)
    fig_.set_title(title)
    fig_.grid(color='black', linestyle=':')
    fig_.legend()  # show legend
    return fig


if __name__ == '__main__':
    root = tk.Tk()
    root.title("IR GUI")
    root.geometry('850x600')
    root.resizable(width=False, height=False)
    frame = tk.Frame(master=root, height=600, width=850)
    frame.place(x=0, y=0, anchor='nw')
    lb = tk.Label(master=root, text='', bg='white')
    lb.place(x=100, y=25, anchor='nw')


    def choose_file():
        file_name = tk.filedialog.askopenfilename()
        if file_name != '':
            lb.config(text="Selected file："+file_name)
            address = file_name
            a = data_open(address)

            def choose(data):
                x = var.get()
                v1_ = float(v1.get())
                v2_ = float(v2.get())
                _a = peak_find(data, v1_, v2_)
                _b = quick_peak_classify(_a)
                if x == '0':
                    return None
                if x == '1':
                    return _a
                if x == '2':
                    return _b

            def _draw(v):
                matplotlib.use('TkAgg')
                import matplotlib.pyplot as plt_
                plt_.rcParams['font.sans-serif'] = ['SimHei']
                # show plot in tkinter window.
                b = choose(a)
                fig__ = _plot(a, b, address)
                canvas = FigureCanvasTkAgg(fig__, master=frame)
                canvas.get_tk_widget().place(x=22, y=10, anchor='nw')

            def _save():
                n = choose(a)
                tit = address.split(r'/')
                tit = tit[-1]
                plot(a, n, title=tit, show=False, save=True, s_f='.png')

            var = tk.StringVar()
            v1 = tk.StringVar()
            v2 = tk.StringVar()
            btn_ = tk.Button(master=root, text='save', command=_save)
            rt1 = tk.Radiobutton(master=frame, text='None', variable=var, value='0',
                                 command=_draw)
            rt2 = tk.Radiobutton(master=frame, text='Peaks only', variable=var, value='1',
                                 command=_draw)
            rt3 = tk.Radiobutton(master=frame, text='show classes', variable=var, value='2',
                                 command=_draw)
            s1 = tk.Scale(master=root, label='threshold', from_=0, to=1.00, orient=tk.HORIZONTAL, variable=v1,
                          length=300, showvalue=1, tickinterval=10, resolution=0.001, command=_draw)
            s2 = tk.Scale(master=root, label='min dist', from_=10, to=1000, orient=tk.HORIZONTAL, variable=v2,
                          length=300, showvalue=1, tickinterval=500, resolution=10, command=_draw)
            btn_.place(x=25, y=480)
            rt1.place(x=25, y=550, anchor='nw')
            rt2.place(x=25, y=530, anchor='nw')
            rt3.place(x=25, y=510, anchor='nw')
            s1.place(x=150, y=515, anchor='nw')
            s2.place(x=515, y=515, anchor='nw')


    btn = tk.Button(master=root, text='choose file', command=choose_file)
    btn.place(x=25, y=25, anchor='nw')
    root.mainloop()
