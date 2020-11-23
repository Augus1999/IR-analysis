# -*- coding: utf-8 -*-
# Author: TAO Nianze (Augus)
import matplotlib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from infraredAnalysis import data_open, peak_find, quick_peak_classify, plot


if __name__ == '__main__':
    root = tk.Tk()
    root.title("IR GUI")
    root.geometry('850x600')
    root.resizable(width=False, height=False)
    frame = tk.Frame(master=root, height=600, width=850)
    frame.place(x=0, y=0, anchor='nw')
    lb = tk.Label(master=root, text='')
    lb.place(x=100, y=25, anchor='nw')


    def choose_file():
        file_name = tk.filedialog.askopenfilename(filetypes=[('CSV', '.csv')])
        if file_name != '':
            lb.config(text="Selected file："+file_name)
            lb['bg'] = 'white'
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
                fig__ = plot(a, b, fig_size=(8.0, 5.0), title=address,
                             show=False, save=False, ret=True)
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
