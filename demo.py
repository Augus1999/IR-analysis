from infraredAnalysis import Frame


a = Frame(r'sample and results\benzoic acid.CSV')
a.plot(title='sample', select=1)
a.print('peak.csv')
