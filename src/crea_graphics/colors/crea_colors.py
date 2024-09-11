# create colormaps from CREA's design guide

import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import colors

from typing import Annotated


def create_continuous_cmap(cmap: ListedColormap, N: int = 200) -> LinearSegmentedColormap:
    """Create continuous colormap from discrete colormap.

    cmap : matplotlib.colors.ListedColormap
        Discrete colormap.
    N : int
        Number of colors in the continuous colormap.

    Returns
    -------
    cmap : matplotlib.colors.LinearSegmentedColormap
        Continuous colormap.
    """

    cmaplist = [cmap(i) for i in range(cmap.N)]

    return LinearSegmentedColormap.from_list(
        cmap.name + "_cont", cmaplist, N)


# # # # # # # # # # # # # # # #
# primary colors
# # # # # # # # # # # # # # # #

N = 7
vals = np.ones((N, 4))*256
vals[0, 0:-1] = [53, 65, 108]   # #35416C
vals[1, 0:-1] = [140, 201, 208]  # 8cc9d0
vals[2, 0:-1] = [204, 231, 235]  # cce7eb
vals[3, 0:-1] = [39, 165, 156]  # #27a59c
vals[4, 0:-1] = [117, 180, 76]  # #75b44c
vals[5, 0:-1] = [51, 51, 51]    # #333333
vals[6, 0:-1] = [202, 202, 202]  # cacaca

vals = vals/256

primary: ListedColormap = ListedColormap(vals, name="primary")

primary_cont: LinearSegmentedColormap = create_continuous_cmap(primary, N=100)
primary_cont_r: LinearSegmentedColormap = create_continuous_cmap(
    ListedColormap(np.flipud(vals)), N=100)


# take the blue colors and add white
vals = np.concatenate((vals[:3, :], np.array([[1, 1, 1, 1]])))
primary_blue = ListedColormap(vals)
primary_blue_cont = create_continuous_cmap(primary_blue, N=100)
primary_blue_cont_r = create_continuous_cmap(
    ListedColormap(np.flipud(vals)), N=100)


# # # # # # # # # # # # # # # #
# colormap for "good vs bad"
# # # # # # # # # # # # # # # #

N = 7
vals = np.ones((N, 4))*256
vals[0, 0:-1] = [53, 65, 108]   # #35416C
vals[1, 0:-1] = [140, 201, 208]  # 8cc9d0
vals[2, 0:-1] = [204, 231, 235]  # cce7eb
vals[3, 0:-1] = [255, 242, 204]  # fff2cc
vals[4, 0:-1] = [246, 178, 107]  # f6b26b
vals[5, 0:-1] = [204, 0, 0]     # #cc0000
vals[6, 0:-1] = [153, 0, 0]     # #990000

vals = vals/256

goodbad: ListedColormap = ListedColormap(vals)

goodbad_cont: LinearSegmentedColormap = create_continuous_cmap(goodbad, N=100)
goodbad_cont_r: LinearSegmentedColormap = create_continuous_cmap(
    ListedColormap(np.flipud(vals)), N=100)

# make continous colormap of the red part of the colormap
goodbad_red_cont = create_continuous_cmap(ListedColormap(vals[3:, :]), N=100)
goodbad_red_cont_r = create_continuous_cmap(
    ListedColormap(np.flipud(vals[3:, :])), N=100)

# make colormap with all but the darkest blue
goodbad_light = create_continuous_cmap(ListedColormap(vals[1:, :]), N=100)
goodbad_light_r = create_continuous_cmap(
    ListedColormap(np.flipud(vals[1:, :])), N=100)


# # # # # # # # # # # # # # # #
# secondary  colors
# # # # # # # # # # # # # # # #

N = 7
vals = np.ones((N, 4))*256

vals[0, 0:-1] = [0, 0, 0]  # 000000
vals[1, 0:-1] = [53, 28, 117]  # 351c75
vals[2, 0:-1] = [116, 27, 71]  # 741b47
vals[3, 0:-1] = [153, 0, 0]  # 990000
vals[4, 0:-1] = [204, 0, 0]  # cc0000
vals[5, 0:-1] = [246, 178, 107]  # f6b26b
vals[6, 0:-1] = [255, 242, 204]  # fff2cc

vals = vals/256

secondary = ListedColormap(vals)
secondary_cont = create_continuous_cmap(secondary, N=100)
secondary_cont_r = create_continuous_cmap(
    ListedColormap(np.flipud(vals)), N=100)

# secondary without black

secondary_noblack = create_continuous_cmap(ListedColormap(vals[1:, :]), N=100)
secondary_noblack_r = create_continuous_cmap(
    ListedColormap(np.flipud(vals[1:, :])), N=100)
