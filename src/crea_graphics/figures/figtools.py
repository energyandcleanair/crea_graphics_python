from PIL import Image
import os

def add_logo(fig, left=0.85, bottom=0.02, logo_scale=1):
    """ Add the CREA logo to the figure.

    Default size of the logo is 10% of the figure width, but can 
    be scaled with logo_scale. Default position for the logo is 
    on the bottom right corner of the figure, but can be
    changed with the left and bottom parameters. The logo is
    added to the figure as an axes, so it can be moved around
    like any other axes.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to which the logo will be added.

    left : float, optional
        The left position of the logo in the figure. Default is 0.85.

    bottom : float, optional
        The bottom position of the logo in the figure. Default is 0.02.

    logo_scale : float, optional
        Parameter to scale the logo size. Default is 1.

    Returns
    -------
    ax_image : matplotlib.axes.Axes
        The axes containing the logo image.
    """

    # Open the image file
    image_in = Image.open(os.path.join(os.path.dirname(__file__), 'LOGO-for graphs.png')) # Open the image
    image = np.array(image_in) # Convert to a numpy array

    # set image size and position
    
    # width is by default 10% of figure width, can be scaled with logo_scale
    width = 0.1 * logo_scale
    # height depends on image aspect ratio
    height =  image.shape[0] / image.shape[1] * width 

    # Add the image to the figure
    ax_image = fig.add_axes([left, bottom, width, height])

    ax_image.imshow(image)
    ax_image.axis('off') 

    return ax_image
