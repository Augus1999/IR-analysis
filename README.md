# IR-analysis
This project is based on numpy, interval, pandas, and peakutils.

Tested on Python 3.7.3 and 3.8.3 (the function batch_plot() only works under Python `3.8` without clear result).

Examples of using ```infraredAnalysis.py``` see ```demo.py```

 Doubleclickrun ```IR_GUI.py``` will start a GUI application based on ```infraredAnalysis.py``` that can directly show the plot, select parameters and save image.

![alt text](https://github.com/Augus1999/IR-analysis/blob/master/sample%20and%20results/example.png)
![alt text](https://github.com/Augus1999/IR-analysis/blob/master/sample%20and%20results/sample.jpg)

The package 'interval' used is a Python file interval.py which, if you use Anaconda, cannot be installed by ```conda install interval```. Install this package by 
```pip install interval```
and copy this file to ```Anaconda\Lib\site-packages```. 'peakutils' does not exist in Anaconda library; install it by ```pip install peakutils``` and copy this package to ```Anaconda\Lib\site-packages```.
