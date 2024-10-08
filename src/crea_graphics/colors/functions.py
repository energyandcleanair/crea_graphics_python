from matplotlib.colors import ListedColormap, LinearSegmentedColormap


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
