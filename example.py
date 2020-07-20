import matplotlib
from infraredAnalysis import Frame
matplotlib.use('Qt5Agg')


a = Frame(r'sample and results\benzoic acid.CSV')
a.plot(title='sample', select=1)
a.print('peak.csv')
