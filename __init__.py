import os
import threading
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
