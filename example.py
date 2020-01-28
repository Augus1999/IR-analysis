from infraredAnalysis import *


a = data_open('sample.CSV')
b = peak_find(a, 0.5, 50)
c = quick_peak_classify(b)
plot(set1=a, set2=c, title='sample', save=True)
peak_data(b, 'peak.csv')
