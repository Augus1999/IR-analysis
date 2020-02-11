import pickle
from interval import Interval


range_class = dict()
range_class['C=O'] = [Interval(1660, 1820)]
range_class['O-H'] = [Interval(3100, 3400)]
range_class['C-O'] = [Interval(1000, 1300)]
range_class['C-H'] = [Interval(2400, 3400)]
range_class['C=C'] = [Interval(1450, 1600)]
range_class['C=N'] = [Interval(1640, 1690)]
range_class['N-H'] = [Interval(3300, 3500)]
range_class['N-H bend'] = [Interval(1550, 1640)]
range_class['C-F'] = [Interval(1000, 1400)]
range_class['C-Cl'] = [Interval(540, 785)]
range_class['C-Br'] = [Interval(500, 667)]
range_class['sat. aldehyde C=O'] = [Interval(1725, 1740)]
range_class['unsat. aldehyde C=O'] = [Interval(1660, 1700)]
range_class['sat. ketone C=O'] = [Interval(1710, 1720)]
range_class['unsat. ketone C=O'] = [Interval(1680, 1700)]
range_class['ring ketone C=O'] = [Interval(1715, 1810)]
range_class['sat. ester C=O'] = [Interval(1735, 1750)]
range_class['unsat. ester C=O'] = [Interval(1715, 1740)]
range_class['ring ester C=O'] = [Interval(1735, 1820)]
range_class['sat. acid C=O'] = [Interval(1700, 1730)]
range_class['unsat. acid C=O'] = [Interval(1715, 1740)]
range_class['ring acid C=O'] = [Interval(1680, 1700)]
range_class['amide C=O'] = [Interval(1630, 1680)]
range_class['alkene C-H stretch'] = [Interval(3000, 3100)]
range_class['alkene C-H bend'] = [Interval(650, 1000)]
range_class['aromatic C-H stretch'] = [Interval(3050, 3150)]
range_class['aromatic C-H bend'] = [Interval(690, 900)]
range_class['nitro group'] = [Interval(1300, 1390), Interval(1500, 1600)]
range_class[r'C$\equiv$C'] = [Interval(2100, 2180)]  # (Latex format) carbon carbon triple bond.
range_class[r'C$\equiv$N'] = [Interval(2150, 2250)]  # (Latex format) carbon nitrogen triple bond.
print(range_class)
with open('ir_peak_range_class.pkl', 'wb') as f:
    pickle.dump(range_class, f)
