from infraredAnalysis import _open, peak_find, quick_peak_classify, plot, peak_data


a = _open('sample.CSV')
b = peak_find(a, 0.5, 50)
c = quick_peak_classify(b)
plot(set1=a, set2=c, title='sample', save=True)
peak_data(b, 'peak.csv')
