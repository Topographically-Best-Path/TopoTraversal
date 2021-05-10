import TopoTraversal.constants as constants
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.colors
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin
import os

# creates new temporary directory for data storage
def create_temp():
    if not os.path.exists(constants.TEMPDIR):
        os.makedirs(constants.TEMPDIR)

# 0 <= lo,la <= 360  1 <= dy,dx <= 5, in degrees
def generate_large_data(lo,la,dy,dx):
    # web scraping
    info = {'north' : str(min(lo+dy,360)), 'south' : str(max(lo-dy,0)), 'east' : str(min(la+dx,360)), 'west' : str(max(la-dx,0)), 'mag' : 1}
    session = HTMLSession()
    url = "https://topex.ucsd.edu/cgi-bin/get_data.cgi"
    url = urljoin(url, "get_data.cgi")
    res = session.post(url, data=info)
    soup = str(BeautifulSoup(res.content, "html.parser"))
    with open(constants.TEMPDIR / 'Data.txt', 'w') as fout:
        fout.write(soup)
    data = np.loadtxt(constants.TEMPDIR / 'Data.txt')
    # configuring data
    Long,Lat,Elev = data[:,0],data[:,1],data[:,2]
    minLong,maxLong = np.min(Long),np.max(Long)
    minLat,maxLat = np.min(Lat),np.max(Lat)
    minElev,maxElev = np.min(Elev),np.max(Elev)
    [x,y] = np.meshgrid(np.linspace(minLong,maxLong,1000),np.linspace(minLat,maxLat,1000))
    z = griddata((Long, Lat), Elev, (x, y), method='linear')
    return [x,y,z] # [degrees,degrees,meters]

# 0 < dy,dx <= 5, in degrees
def get_scale(dy,dx):
    vertical = 40070 * ((2*dy)/360) / 1000 * 1000
    horizontal = 40070 * ((2*dx)/360) / 1000 * 1000
    diagonal = Math.sqrt(vertical*vertical + horizontal*horizontal)
    return [vertical,horizontal,diagonal] # [meters,meters,meters]

# x,y,z are 2d ndarrays of the same shape.
def generate_image(x,y,z):
    # color map creation
    class FixPointNormalize(matplotlib.colors.Normalize):
        def __init__(self, vmin=None, vmax=None, sealevel=0, col_val = 0.21875, clip=False):
            self.sealevel = sealevel
            self.col_val = col_val
            matplotlib.colors.Normalize.__init__(self, vmin, vmax, clip)
        def __call__(self, value, clip=None):
            x, y = [self.vmin, self.sealevel, self.vmax], [0, self.col_val, 1]
            return np.ma.masked_array(np.interp(value, x, y))
    colors_undersea = plt.cm.terrain(np.linspace(0, 0.22, 69))
    colors_land = plt.cm.terrain(np.linspace(0.25, 1, 228))
    colors = np.vstack((colors_undersea, colors_land))
    cut_terrain_map = matplotlib.colors.LinearSegmentedColormap.from_list('cut_terrain', colors)
    # graphing and saving image
    x = np.matrix.flatten(x)
    y = np.matrix.flatten(y)
    z = np.matrix.flatten(z)
    minLong,maxLong = np.min(x),np.max(x)
    minLat,maxLat = np.min(y),np.max(y)
    minElev,maxElev = np.min(z),np.max(z)
    fig,ax = plt.subplots()
    ax.set_axis_off()
    norm = FixPointNormalize(sealevel=0,vmax=maxElev,vmin=minElev)
    plt.scatter(x,y,1,z,cmap=cut_terrain_map,norm=norm)
    plt.gca().set_aspect('equal')
    plt.xlim(minLong,maxLong)
    plt.ylim(minLat,maxLat)
    plt.savefig(constants.TEMPDIR / "Image.png", bbox_inches='tight', pad_inches=0)
