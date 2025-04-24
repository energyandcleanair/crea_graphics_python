import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.enums import Resampling
import xarray as xr


def write_cog(da, vmin=None, vmax=None, cmap=None, output_path='output_cog.tif',
              no_alpha=False, alpha_var=None, alpha_range=None, project_to=None,
              resampling='nearest'):
    """
    Write a DataArray to a Cloud Optimized GeoTIFF

    Parameters
    ----------
    da : xarray.DataArray
        The DataArray to write to a GeoTIFF
    vmin : float, optional
        The minimum value to use for normalization
    vmax : float, optional
        The maximum value to use for normalization
    cmap : str, optional
        The name of the colormap to use. As default, using 'viridis'.
    output_path : str, optional
        The path to write the GeoTIFF
    resampling : str, optional
        The resampling method to use when generating different overview 
        levels. Default is 'nearest'. For info see https://guide.cloudnativegeo.org/cloud-optimized-geotiffs/cogs-overview_resampling.html
    """

    # take a copy of the dataarray to avoid modifying the original
    # (could cause unwanted side effects in calling code)
    dataarray = da.copy()

    if project_to is not None:
        # reproject the data to requested projection
        dataarray = dataarray.rio.reproject(project_to)
        if alpha_var is not None:
            alpha_var = alpha_var.rio.reproject(project_to)
    else:
        # by default, data should be outputted in EPSG:3857
        dataarray = dataarray.rio.reproject("EPSG:3857")

    # xr.where looses attributes, including crs info
    crs_out = dataarray.rio.crs
    transform_out = dataarray.rio.transform()

    # Normalize the data to the range 0-1 for colormap application
    if vmin is None:
        vmin = dataarray.min().values
    else:
        # set all values below vmin to vmin
        dataarray = xr.where(dataarray < vmin, vmin,
                             dataarray, keep_attrs=True)

    if vmax is None:
        vmax = dataarray.max().values
    else:
        # set all values above vmax to vmax
        dataarray = xr.where(dataarray > vmax, vmax, dataarray)

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=True)

    # Choose a colormap
    if cmap is None:
        cmap = 'viridis'
    cmap = plt.get_cmap(cmap)

    # Apply the colormap to the normalized data to get RGBA values
    rgba_data = cmap(norm(dataarray))
    ind_nan = np.isnan(dataarray)

    # Convert RGBA to RGB (drop the alpha channel), if requested
    if no_alpha:
        # Shape will be (height, width, 3)
        rgb_data = np.delete(rgba_data, 3, 2)
    else:
        rgb_data = rgba_data

    # Transpose the RGB data to match the shape (bands, height, width)
    rgb_data = np.transpose(rgb_data, (2, 0, 1))

    # Scale the data to 0-255
    rgb_data = (rgb_data * 255)

    # if alpha variable given, make transparency dependent on alpha variable
    if alpha_var is not None:
        # Normalize the data to the range 0-1 to use for transparency
        if alpha_range is None:
            alpha_range = [alpha_var.min().values, alpha_var.max().values]

        # normalize between alpha_range[0] and alpha_range[1]
        alpha_var = xr.where(
            alpha_var < alpha_range[0], alpha_range[0], alpha_var)
        alpha_var = xr.where(
            alpha_var > alpha_range[1], alpha_range[1], alpha_var)
        norm_alpha = (alpha_var - alpha_range[0]) / \
            (alpha_range[1] - alpha_range[0])

        rgb_data[-1, :] = (norm_alpha * 255).astype('uint8')

    # set nan values to white
    rgb_data[:3, ind_nan] = 255
    # for white color, set alpha to 0
    if not no_alpha:
        rgb_data[-1, ind_nan] = 0

    # convert to uint8 data type for writing to GeoTIFF
    rgb_data = rgb_data.astype('uint8')

    # Define the metadata for the GeoTIFF
    metadata = {
        'driver': 'GTiff',
        'dtype': 'uint8',
        'nodata': None,
        'width': rgb_data.shape[2],
        'height': rgb_data.shape[1],
        'count': len(rgb_data[:, 0, 0]),
        'crs': crs_out,  # da.rio.crs,
        'transform': transform_out,  # da.rio.transform(),
        'compress': 'DEFLATE',
        'tiled': True,
        'blockxsize': 256,
        'blockysize': 256,
        'BIGTIFF': 'IF_SAFER'
    }

    # Write the RGB data to a Cloud Optimized GeoTIFF
    with rasterio.open(output_path, 'w', **metadata) as dst:
        dst.write(rgb_data)

        # Add overviews
        dst.build_overviews([2, 4, 8, 16], Resampling.nearest)
        dst.update_tags(ns='rio_overview', resampling='nearest')
