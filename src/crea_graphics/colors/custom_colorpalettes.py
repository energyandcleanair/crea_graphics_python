# other custom color palettes, not based on crea colors

import numpy as np
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from src.crea_graphics.colors.functions import create_continuous_cmap


# Taking the colors YlGnBu from ColorBrewer (https://colorbrewer2.org/#type=sequential&scheme=YlGnBu&n=9)
# and adding some more darker colors, ending with black


vals = np.array([[255, 255, 217],
                 [237, 248, 177],
                 [199, 233, 180],
                 [127, 205, 187],
                 [65, 182, 196],
                 [29, 145, 192],
                 [34, 94, 168],
                 [37, 52, 148],
                 [8, 29, 88],
                 [6, 23, 70],
                 [3, 10, 35],
                 [0, 0, 0]  # black
                 ])

vals = vals / 256.0

ylgnbubl = create_continuous_cmap(ListedColormap(vals), N=250)
