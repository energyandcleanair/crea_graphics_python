## Using colormaps

To use CREA color palettes, for example the goodbad colors, in your python code:

    from crea_graphics.colors import goodbad

`goodbad` is a matplotlib.colors.ListedColormap object, and can be passed to the cmap argument when making figures.

For continuous colormap, to use with raster image:

      from crea_graphics.colors import goodbad_cont

`goodbad_cont` is a matplotlib.colors.LinearSegmentedColormap object, which also can be passed to the cmap argument. For example:

      plt.pcolormesh(..., cmap=goodbad_cont)
