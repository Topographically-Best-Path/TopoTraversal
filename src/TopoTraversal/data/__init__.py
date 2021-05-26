import TopoTraversal.constants as constants
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.colors
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import os
import math

# PARAMETERS: none
# RETURN VALUE: none
# PURPOSE: creates new temporary directory for data and image storage
def create_temp():
    if not os.path.exists(constants.TEMPDIR):
        os.makedirs(constants.TEMPDIR)

# PARAMETERS: 0 <= lo,la <= 360  1 <= dy,dx <= 5, in degrees
# RETURN VALUE: [x,y,z], each are 1000x1000 np arrays, [degrees,degrees,meters]
# PURPOSE: generates a uniform 1000x1000 dataset to be later used in image generation and best path creation
def generate_large_data(lo,la,dy,dx):
    # generating form responses based on parameters
    info = {'north' : str(min(lo+dy,360)), 'south' : str(max(lo-dy,0)), 'east' : str(min(la+dx,360)), 'west' : str(max(la-dx,0)), 'mag' : 1}

    # starting html session and navigating to website
    session = HTMLSession()
    url = urljoin(constants.URL1, "get_data.cgi")

    # submitting form and obtaining the resulting data
    res = session.post(url, data=info)
    soup = str(BeautifulSoup(res.content, "html.parser"))

    # saving data to temporary directory, temporary directory needs to be made first
    with open(constants.TEMPDIR / 'Data.txt', 'w') as fout:
        fout.write(soup)

    # loading data from the temporary directory into an np array
    data = np.loadtxt(constants.TEMPDIR / 'Data.txt')

    # separating combined data into their respective data sets
    Long,Lat,Elev = data[:,0],data[:,1],data[:,2]

    # finding mininums and maximums of respective datasets
    minLong,maxLong = np.min(Long),np.max(Long)
    minLat,maxLat = np.min(Lat),np.max(Lat)
    minElev,maxElev = np.min(Elev),np.max(Elev)

    # scaling the data into a uniform 1000x1000 np array
    [x,y] = np.meshgrid(np.linspace(minLong,maxLong,1000),np.linspace(minLat,maxLat,1000))
    z = griddata((Long, Lat), Elev, (x, y), method='linear')

     # returning final data set
    return [x,y,z]

# PARAMETERS: 0 < dy,dx <= 5, in degrees
# RETURN VALUE: [v,h,d], floating points numbers, [meters, meters, meters]
# PURPOSE: finds the distances between two horizontally, vertically, or diagonally separated points, to be later used in the best path algorithm
def get_scale(dy,dx):
    # converting distances from degrees to meters
    vertical = 40070 * ((2*dy)/360) / 1000 * 1000
    horizontal = 40070 * ((2*dx)/360) / 1000 * 1000

    # creating diagonal distance from pythagorean theorem
    diagonal = math.sqrt(vertical*vertical + horizontal*horizontal)

    # returning calculated values
    return [vertical,horizontal,diagonal]

# PARAMETERS: x,y,z are 2d ndarrays of the same shape, should be taken from one of the generate data functions above
# RETURN VALUE: none
# PURPOSE: creates a topographic image that is saved in the temp directory, to be later displayed to the user
def generate_image(x,y,z):
    # class to help smooth out the color map that will be used in the image generation
    class FixPointNormalize(matplotlib.colors.Normalize):
        # obtaining data from regular matplotlib normalize library
        def __init__(self, vmin=None, vmax=None, sealevel=0, col_val = 0.21875, clip=False):
            self.sealevel = sealevel
            self.col_val = col_val
            matplotlib.colors.Normalize.__init__(self, vmin, vmax, clip)

        # smoothing out given data and returning it
        def __call__(self, value, clip=None):
            x, y = [self.vmin, self.sealevel, self.vmax], [0, self.col_val, 1]
            return np.ma.masked_array(np.interp(value, x, y))

    # obtaining specific color gradients from matplotlib
    colors_undersea = plt.cm.terrain(np.linspace(0, 0.22, 69))
    colors_land = plt.cm.terrain(np.linspace(0.25, 1, 228))

    # combining land and undersea gradients into one gradient
    colors = np.vstack((colors_undersea, colors_land))

    # creating color map from color gradients
    cut_terrain_map = matplotlib.colors.LinearSegmentedColormap.from_list('cut_terrain', colors)

    # flattening out data into 1d np arrays so they can be graphed
    x = np.matrix.flatten(x)
    y = np.matrix.flatten(y)
    z = np.matrix.flatten(z)

    # finding mininums and maximums of respective datasets
    minLong,maxLong = np.min(x),np.max(x)
    minLat,maxLat = np.min(y),np.max(y)
    minElev,maxElev = np.min(z),np.max(z)

    # creating figure and removing axes
    fig,ax = plt.subplots()
    ax.set_axis_off()

    # creating data that will help normalize the color map
    norm = FixPointNormalize(sealevel=0,vmax=maxElev,vmin=minElev)

    # plotting all the datasets into the figure 
    plt.scatter(x,y,1,z,cmap=cut_terrain_map,norm=norm)

    # changing the scale and limits of the figure
    plt.gca().set_aspect('equal')
    plt.xlim(minLong,maxLong)
    plt.ylim(minLat,maxLat)

    # saving final figure into the temporary directory
    plt.savefig(constants.TEMPDIR / "Image.png", bbox_inches='tight', pad_inches=0)
